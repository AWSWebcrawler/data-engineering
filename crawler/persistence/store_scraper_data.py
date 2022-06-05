"""Stores the product as csv or in S3

    receives a product_dict with all values and the settings_dict
    with the wanted settings e.g. where to store"""

import csv
import logging
from os.path import exists
from datetime import datetime as dt, timedelta, timezone
import boto3
from crawler.exceptions.exceptions_config_reader import CouldNotWriteToFileError
from crawler.logging.decorator import decorator_for_logging


@decorator_for_logging
def store_item(product_dict: dict, settings_dict: dict) -> None:
    """Method receives an item to be stored. It uses environment variables to determine
    whether storage in AWS S3 bucket or local in csv file is required"""
    header_list = [
        "timestamp",
        "date",
        "time",
        "name",
        "current_price",
        "price_regular",
        "prime",
        "discount_in_euros",
        "percent_discount",
        "sold_by_amazon",
        "seller",
        "brand",
        "shipping",
        "amazon_choice",
        "amazon_choice_for",
        "asin",
        "product_id",
        "manufacturer",
        "country_of_origin",
        "product_dimensions",
        "number_of_reviews",
        "review_score",
        "on_sale_since",
        "url",
    ]
    if settings_dict["aws_env"]:
        store_to_s3(product_dict, settings_dict, header_list)
    else:
        filepath = "../output/" + settings_dict["client"] + ".csv"
        store_to_csv(product_dict, filepath, header_list)


@decorator_for_logging
def store_to_csv(product_output_list: list, filepath: str, header_list: list) -> None:
    """Gets called by store_item with a list of product dictionaries
    containing product information
    and stores the products as lines in a csv file"""
    file_exists = exists(filepath)
    logging.debug("File in filepath: %s exists: %s", filepath, str(file_exists))
    with open(filepath, 'a', encoding='utf-8', newline='') as file:
        try:
            writer = csv.writer(file)
            if file_exists:
                pass
            else:
                writer.writerow(header_list)

            for product_dict in product_output_list:
                write_values = []
                for header in header_list:
                    value = product_dict[header]
                    if isinstance(value, str):
                        value = value.replace(",", "")
                        value = value.replace('"', "").replace("'", "")
                        value.strip()
                    write_values.append(value)
                writer.writerow(write_values)
        except Exception:
            logging.error("Could not write file")
            raise CouldNotWriteToFileError from Exception(
                "Could not write the file or append values to list"
            )
        file.close()


@decorator_for_logging
def store_to_s3(product_dict: dict, settings_dict: dict, headers: list) -> None:
    """Method gets an product dictionary and the name of the used client.
    Items from the product_dict are then
    stored in S3 in CSV format."""

    bucket_name = settings_dict["s3_bucket"]
    now = dt.now(timezone(timedelta(hours=2)))
    s3_filename = f"ScraperData/" \
                  f"{str(now.year)}/" \
                  f"{str(now.month)}/" \
                  f"{str(now.day)}/" \
                  f"{str(now.hour)}/" \
                  f"{str(now.minute)}/" \
                  f"{settings_dict['client']}_lambda.csv"
    local_file = "/tmp/download.csv"
    s3 = boto3.resource("s3")
    logging.debug("writing to bucket %s with filename %s", bucket_name, s3_filename)
    body = ""

    for item in headers:
        body += \
            str(product_dict[item]).replace(',', '').replace('"', '').replace("'", '')
        if item != headers[-1]:
            body += ","
    body += "\n"

    with open(local_file, mode="w", encoding="utf-8") as file:
        empty_test_char = file.read(1)
        if empty_test_char:
            column_names = ""
            for item in headers:
                column_names += item
                if item != headers[-1]:
                    column_names += ","
            column_names += "\n"
            file.write(column_names)
        file.write(body)

    s3.meta.client.upload_file(local_file, bucket_name, s3_filename)