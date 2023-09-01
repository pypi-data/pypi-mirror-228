import click
import json
import zipfile
from jinja2 import Environment, FileSystemLoader
import os
import pandas
import subprocess
import requests
import webbrowser
import subprocess
from urllib.parse import urlparse, parse_qs
import asyncio
import shutil
import importlib
import importlib.util
import yaml
from analysis_usedecorator import (
    convert_notebook_to_python,
    get_functions_with_decorator,
    create_struture_template,
    write_resource_package,
    retrieve,
)
from datapeach_wrapper.wrapper import dp_import, dp_function, set_ignore_dp_config

host = "localhost"
port = 9000


@click.group()
def cli():
    pass


async def wait_for_login(preAuthSessionId: str):
    invoked_url = f"http://{host}:{port}/waitforlogin"
    payload = {"preAuthSessionId": preAuthSessionId}
    headers = {"Accept": "application/json"}
    response = requests.request("POST", invoked_url, headers=headers, json=payload)

    click.echo(f"response: {response.text}")
    if response.text == '"Not consumed"':
        click.echo(f"true: {response.text}")
        while True:
            await asyncio.sleep(5)
            return await wait_for_login(preAuthSessionId)
    else:
        return response.text


def check_empty_value(ctx, param, value):
    if len(value) == 0 or value.isspace():
        raise click.ClickException(
            "Can not input a whitespace character or an empty string"
        )
    else:
        return value


@cli.command(name="template")
@click.argument("create", required=1, type=click.Choice(["create"]))
@click.option(
    "-o",
    "--output_template_folder_path",
    callback=check_empty_value,
    prompt="Enter output template folder path",
    help="The output template folder path",
)
# @click.option("-n", "--name", callback=check_empty_value, prompt="Enter name", help="The name of the function")
@click.option(
    "-t",
    "--title",
    callback=check_empty_value,
    prompt="Enter title",
    help="The title of the function",
)
@click.option(
    "-v",
    "--version",
    callback=check_empty_value,
    prompt="Enter version",
    help="The version of the function",
)
# @click.option("-s", "--namespace", callback=check_empty_value, prompt="Enter namespace", help="The namespace of the function")
@click.option(
    "-e",
    "--execution_mode",
    callback=check_empty_value,
    type=click.Choice(["sync", "async"], case_sensitive=False),
    prompt="Enter execution mode",
    help="The execution mode of the function",
)
def generic(create, output_template_folder_path, title, version, execution_mode):
    # click.echo(f'output_template_folder_path: {output_template_folder_path}')

    env = Environment(loader=FileSystemLoader(["templates", "templates/src"]))
    setupTemplate = env.get_template("setup.j2")
    requirementsTemplate = env.get_template("requirements.txt")
    licenseTemplate = env.get_template("LICENSE")
    readmeTemplate = env.get_template("README.md")
    mainTemplate = env.get_template("main.py")
    mainAsyncTemplate = env.get_template("main_async.py")
    initTemplate = env.get_template("__init__.py")

    try:
        # raise "InvalidAgeException"
        output_template_folder_path = output_template_folder_path.replace("\\", "/")
        if not os.path.exists(output_template_folder_path):
            os.makedirs(output_template_folder_path)
        name = title.strip().replace(" ", "_")
        if not os.path.exists(f"{output_template_folder_path}/{name}"):
            os.mkdir(f"{output_template_folder_path}/{name}")

        setupFunctionContext = {
            "name": name,
            "version": version,
            "title": title,
            "execution_mode": execution_mode,
        }
        with open(
            f"{output_template_folder_path}/{name}/setup.yml",
            mode="w",
            encoding="utf-8",
        ) as results:
            results.write(setupTemplate.render(setupFunctionContext))
        with open(
            f"{output_template_folder_path}/{name}/requirements.txt",
            mode="w",
            encoding="utf-8",
        ) as results:
            results.write(requirementsTemplate.render())
        with open(
            f"{output_template_folder_path}/{name}/LICENSE", mode="w", encoding="utf-8"
        ) as results:
            results.write(licenseTemplate.render())
        with open(
            f"{output_template_folder_path}/{name}/README.md",
            mode="w",
            encoding="utf-8",
        ) as results:
            results.write(readmeTemplate.render())
        if not os.path.exists(f"{output_template_folder_path}/{name}/src"):
            os.mkdir(f"{output_template_folder_path}/{name}/src")
        with open(
            f"{output_template_folder_path}/{name}/src/__init__.py",
            mode="w",
            encoding="utf-8",
        ) as results:
            results.write(initTemplate.render())
        if execution_mode == "sync":
            with open(
                f"{output_template_folder_path}/{name}/src/main.py",
                mode="w",
                encoding="utf-8",
            ) as results:
                results.write(mainTemplate.render())
        elif execution_mode == "async":
            with open(
                f"{output_template_folder_path}/{name}/src/main.py",
                mode="w",
                encoding="utf-8",
            ) as results:
                results.write(mainAsyncTemplate.render())

        click.echo(f"Generated")

        vscode_path = shutil.which("code")
        subprocess.run([vscode_path or "", f"{output_template_folder_path}/{name}"])
    except Exception as exc:
        click.echo(f"Error: {exc}")


def zip_function(function_folder_path: str, file_name: str):
    if not os.path.exists(function_folder_path):
        raise Exception(f"Function '{function_folder_path}' does not exist")

    tmpFolder = "tmp"
    if not os.path.exists(tmpFolder):
        os.makedirs(tmpFolder)

    zip_file = f"{tmpFolder}/{file_name}.zip"
    ignore_folders = [".vscode", ".venv"]

    with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zf:
        # Walk through the folder and its contents
        for root, dirs, files in os.walk(function_folder_path):
            # Exclude ignored folders from further traversal
            dirs[:] = [d for d in dirs if d not in ignore_folders]
            for file in files:
                # Create the relative path
                relative_path = os.path.relpath(
                    os.path.join(root, file), function_folder_path
                )
                # Add the file to the zip file
                zf.write(os.path.join(root, file), arcname=relative_path)
    click.echo(f"Folder '{function_folder_path}' zipped successfully")
    return zip_file


@cli.command(name="notebook")
@click.argument("__import__", required=1, type=click.Choice(["import"]))
@click.option(
    "-f",
    "--input_jupyter_notebook_file_path",
    callback=check_empty_value,
    prompt="Enter input jupyter notebook file path",
    help="The  input jupyter notebook file path",
)
def jupyter_notebook_generic(__import__, input_jupyter_notebook_file_path):
    # Wrapper process
    destination_folder = "dist"
    if not os.path.exists(destination_folder):
        os.mkdir(destination_folder)
    zip_file = None
    try:
        set_ignore_dp_config(True)
        """fake args file path"""
        # input_jupyter_notebook_file_path = 'usedecorator_2.ipynb'
        input_jupyter_notebook_file_path = input_jupyter_notebook_file_path.replace(
            "\\", "/"
        )
        if not os.path.exists(input_jupyter_notebook_file_path):
            input_jupyter_notebook_file_path = "datapeach_wrapper/usedecorator_2.ipynb"

        python_file_name, _ = os.path.splitext(input_jupyter_notebook_file_path)
        python_file = python_file_name + ".py"
        convert_notebook_to_python(input_jupyter_notebook_file_path, python_file)

        # module_name = 'usedecorator'
        # Import the module dynamically
        spec = importlib.util.spec_from_file_location(python_file_name, python_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        functions_with_decorator_import = get_functions_with_decorator(
            module, dp_import
        )
        functions_with_decorator = get_functions_with_decorator(module, dp_function)

        # call structure template
        dict_args: dict = create_struture_template(
            functions_with_decorator[0], destination_folder
        )
        destination_folder = destination_folder + "/" + dict_args["name"]
        for func in functions_with_decorator_import:
            retrieve(func, destination_folder)

        for func in functions_with_decorator:
            retrieve(func, destination_folder)

        # file_path = os.path.join(absolute_path, "usedecorator.py")

        search_text = "import "
        dir_main_file = destination_folder + "/src/main.py"
        with open(python_file, "r") as file:
            for line_number, line in enumerate(file, start=1):
                if search_text in line:
                    if (
                        "from datapeach_wrapper.wrapper " in line
                        or "import datapeach_wrapper.wrapper " in line
                    ):
                        continue
                    with open(dir_main_file, "r") as file:
                        content = file.read()
                    new_content = line.rstrip() + "\n" + content
                    with open(os.path.join(dir_main_file), "w") as file:
                        file.write(new_content)
                    # print(f"Found '{search_text}' at line {line_number}: {line.rstrip()}")

        """write cotent setup.yml file"""
        info_setup = """
            {
            "info": {
                "name": "DpFunction",
                "version": "1.0.0",
                "title": "DataPeach Function"
            },
            "runtime": {
                "name": "__main__"
            },
            "configuration": {
                "execution_mode": "sync"
            },
            "setting": {
                "properties": null
            }
            }
        """
        data_info_setup = json.loads(info_setup)
        # print(data_info_setup)
        # print(type(data_info_setup))
        data_info_setup["info"]["name"] = dict_args["name"]
        data_info_setup["info"]["title"] = dict_args["title"]
        data_info_setup["info"]["version"] = dict_args["version"]

        setup_yml = getattr(module, "__setup__")
        # print(type(setup_yml()))
        json_setup = setup_yml()
        # print(type(json_setup))

        # print(setup_yml())
        address_object = data_info_setup["setting"]
        address_object["properties"] = json_setup

        file_path_yml = destination_folder + "/setup.yml"
        # Write the data to the YAML file
        with open(file_path_yml, "w") as file:
            yaml.dump(data_info_setup, file)

        """list all package requirement"""
        write_resource_package(python_file, destination_folder)
        print(f"dict_args: {dict_args}")
        # except Exception as exc:
        #     click.echo(f'Error: {exc}')

        # function_folder_path = dict_args["name"]

        # Zip Process
        # try:
        zip_file = zip_function(destination_folder, dict_args["name"])
        # except Exception as exc:
        #     click.echo(
        #         f"Error: Folder '{dict_args['name']}' can not zip because '{exc}'")
        #     return

        # # Import process
        # try:
        invoked_url = f"http://{host}:{port}/api/v1/functions/upload/"
        dt_conf_file = "credentials.json"
        with open(dt_conf_file, "r") as conf_file:
            dt_config = json.load(conf_file)
        access_key = dt_config["access_key"]
        secret_key = dt_config["secret_key"]
        payload = {}
        headers = {
            "Accept": "application/json",
            "credentials": f"{access_key};{secret_key}",
        }
        # headers["authorization"] = f'Bearer {token}'
        files = [
            (
                "file",
                (f"{dict_args['name']}.zip", open(zip_file, "rb"), "application/zip"),
            )
        ]
        response = requests.request(
            "POST", invoked_url, headers=headers, data=payload, files=files
        )
        if response.ok:
            click.echo(f"Imported")
        else:
            raise Exception(json.loads(response.text)["message"])
    except Exception as exc:
        click.echo(f"Error: '{exc}'")
        return
    finally:
        set_ignore_dp_config(False)
        if os.path.exists(destination_folder):
            shutil.rmtree(destination_folder)
        if zip_file and os.path.exists(zip_file):
            os.remove(zip_file)


@cli.command(name="authentication")
@click.argument("__import__", required=1, type=click.Choice(["login"]))
def super_token_authenticate(__import__):
    # Import process
    try:
        host = "localhost"
        port = 9000
        invoked_url = f"http://{host}:{port}/getmagiclink"
        response = requests.request("GET", invoked_url)
        if response.ok:
            click.echo(response.text)
            webbrowser.open(response.text)
            url_parts = urlparse(response.text)
            query_parameters = parse_qs(response.text)
            preAuthSessionId = query_parameters.get("preAuthSessionId", [""])[0]
            click.echo(f"preAuthSessionId: {preAuthSessionId}")
            jwt = asyncio.run(wait_for_login(preAuthSessionId))

            click.echo(f"jwt: {jwt}")

        else:
            raise Exception(json.loads(response.text)["message"])
    except Exception as exc:
        click.echo(f"Error: '{exc}'")
        return


@cli.command(name="credential")
@click.argument("__import__", required=1, type=click.Choice(["import"]))
@click.option(
    "-f",
    "--credential_file_path",
    callback=check_empty_value,
    prompt="Enter credential file path",
    help="The credential file path",
)
def import_credential(__import__, credential_file_path):
    try:
        credential_file_path = credential_file_path.replace("\\", "/")
        if not os.path.exists(credential_file_path):
            raise Exception(
                "File does not exist. Please take It from DataPeach website and put It to the root folder."
            )
        else:
            with open(credential_file_path, "r") as input_file:
                content = input_file.read()
            with open("credentials.json", "w") as output_file:
                output_file.write(content)
            click.echo(f"Credential file was imported")
    except Exception as exc:
        click.echo(f"Error: {exc}")
        return


@cli.command(name="function")
@click.argument("__import__", required=1, type=click.Choice(["import"]))
@click.option(
    "-f",
    "--input_template_folder_path",
    callback=check_empty_value,
    prompt="Enter input template folder path",
    help="The input template folder path",
)
def import_template(__import__, input_template_folder_path):
    # Check existence of credentials.json file
    try:
        if not os.path.exists("credentials.json"):
            raise Exception(
                "credentials.json file does not exist. Please take It from Datapeach website and use datapeach credential import cli to update credential."
            )
    except Exception as exc:
        click.echo(f"Error: {exc}")
        return

    # Zip Process
    try:
        folder_path_org = input_template_folder_path.replace("\\", "/")
        file_name = [
            d for d in os.listdir(folder_path_org) if not d.endswith((".zip"))
        ][0]
        folder_path = f"{folder_path_org}/{file_name}"
        zip_file = f"{folder_path_org}/{file_name}.zip"
        ignore_folders = [".vscode", ".venv"]
        if not os.path.exists(folder_path_org):
            raise Exception(f"Folder '{folder_path_org}' does not exist")

        with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zf:
            # Walk through the folder and its contents
            for root, dirs, files in os.walk(folder_path):
                # Exclude ignored folders from further traversal
                dirs[:] = [d for d in dirs if d not in ignore_folders]
                for file in files:
                    # Create the relative path
                    relative_path = os.path.relpath(
                        os.path.join(root, file), folder_path
                    )
                    # Add the file to the zip file
                    zf.write(os.path.join(root, file), arcname=relative_path)
        click.echo(f"Folder '{input_template_folder_path}' zipped successfully")
    except Exception as exc:
        click.echo(
            f"Error: Folder '{input_template_folder_path}' can not zip because '{exc}'"
        )
        return

    # Import process
    try:
        invoked_url = f"http://{host}:{port}/api/v1/functions/upload/"
        dt_conf_file = "credentials.json"
        with open(dt_conf_file, "r") as conf_file:
            dt_config = json.load(conf_file)
        access_key = dt_config["access_key"]
        secret_key = dt_config["secret_key"]
        payload = {}
        headers = {
            "Accept": "application/json",
            "credentials": f"{access_key};{secret_key}",
        }
        # headers["authorization"] = f'Bearer {token}'
        files = [
            (
                "file",
                (
                    f"{file_name}.zip",
                    open(f"{folder_path_org}/{file_name}.zip", "rb"),
                    "application/zip",
                ),
            )
        ]
        response = requests.request(
            "POST", invoked_url, headers=headers, data=payload, files=files
        )
        if response.ok:
            click.echo(f"Imported")
        else:
            raise Exception(json.loads(response.text)["message"])
    except Exception as exc:
        click.echo(f"Error: '{exc}'")
        return


if __name__ == "__main__":
    cli(prog_name="datapeach")
