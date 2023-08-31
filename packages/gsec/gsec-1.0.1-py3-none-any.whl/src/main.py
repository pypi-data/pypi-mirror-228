import click, datetime, json, subprocess, os
from cryptography.fernet import Fernet
from src.colors import *
from src.config import repo_dir, config_path

key = os.getenv("SECRET_KEY")
if not key:
    os.chdir(config_path)
    if not os.path.exists(".key"):
        key = Fernet.generate_key()
        with open(".key", "wb") as f:
            f.write(key)
    else:
        with open(".key", "rb") as f:
            key = f.read()

os.chdir(repo_dir())

if not os.path.exists(".git"):
    subprocess.run(["git", "init"])

gh_version = subprocess.run(["gh", "--version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if gh_version.returncode != 0:
    print("GitHub CLI is not installed. Please install it.")
    exit(1)

try:
    fernet = Fernet(key)
except Exception as e:
    print(RED+"[-] Error: "+RESET, e)
    print(GREEN+"[+]"+GRAY+" Please delete the "+CYAN+".key"+GRAY+" file or remove the "+CYAN+ "SECRET_KEY"+GRAY+" environment variable.")
    exit(1)

def encrypt(string):
    return fernet.encrypt(string.encode())

def decrypt(string):
    return fernet.decrypt(string.encode()).decode()

@click.group()
def cli():
    pass

@cli.command()
@click.argument("secret", nargs=-1)
@click.option("--dont-enc-title", "-det", help="Don't encrypt the title of the issue", is_flag=True, default=False)
@click.option("--title", "-t", default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), help="Title of the issue")
def add(secret, title, dont_enc_title):
    ''' Add a new secret '''
    secret = " ".join(secret)
    encSecret = encrypt(secret)
    if not dont_enc_title:
        title = encrypt(title).decode()
    create_issue = subprocess.run(["gh", "issue", "create", "--title", title, "--body", encSecret.decode()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if create_issue.returncode != 0:
        print(create_issue.stderr.decode())
        exit(1)
    click.echo(create_issue.stdout.decode())

@cli.command()
def list():
    ''' List all secrets '''
    list_issues = subprocess.run(["gh", "issue", "list", "--json", "title,number"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if list_issues.returncode != 0:
        print(list_issues.stderr.decode())
        exit(1)
    for i in json.loads(list_issues.stdout.decode()):
        try:
            decTitle = decrypt(i["title"])
            i["title"] = decTitle
        except Exception as e:
            pass
        click.echo(f">> {CYAN}{i['number']}{RESET}: {i['title']}")

@cli.command()
@click.argument("issue_id")
def delete(issue_id):
    ''' Delete a secret by ID'''
    if not click.confirm("Are you sure you want to delete this issue?"):
        exit(0)
    del_issue = subprocess.run(["gh", "issue", "delete", issue_id], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if del_issue.returncode != 0:
        print(del_issue.stderr.decode())
        exit(1)
    click.echo(del_issue.stdout.decode())

@cli.command()
@click.argument("issue_id")
def show(issue_id):
    ''' Show a secret by ID'''
    show_issue = subprocess.run(["gh", "issue", "view", issue_id], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if show_issue.returncode != 0:
        print(show_issue.stderr.decode())
        exit(1)
    c = show_issue.stdout.decode()

    try:
        Title = decrypt(c.split("\n")[0].split(":")[-1].strip())
        #c = c.replace(c.split("\n")[0].split(":")[-1].strip(), Title)
    except Exception as e:
        Title = c.split("\n")[0].split(":")[-1].strip()  

    try:
        Desc = decrypt(c.split("\n")[-2])
        #c = c.replace(c.split("\n")[-2], Desc)
    except Exception as e:
        Desc = c.split("\n")[-2]

    #click.echo(c)
    click.echo(f"{CYAN}{issue_id}{RESET}: {Title}\n---\n{Desc}")

@cli.command()
@click.argument("issue_id")
@click.argument("secret", nargs=-1)
@click.option("--title", "-t", help="Title of the issue")
def edit(issue_id, secret, title):
    ''' Edit a secret by ID'''
    secret = " ".join(secret)
    encSecret = encrypt(secret)

    if title:
        edit_issue = subprocess.run(["gh", "issue", "edit", issue_id, "--title", title, "--body", encSecret.decode()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        edit_issue = subprocess.run(["gh", "issue", "edit", issue_id, "--body", encSecret.decode()], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    if edit_issue.returncode != 0:
        print(edit_issue.stderr.decode())
        exit(1)
    click.echo(edit_issue.stdout.decode())

if __name__ == "__main__":
    cli()