#:coding=utf-8:

import os
import argparse

import django
from django.core.management import call_command

from waitress import serve

from homepage import __version__ as VERSION
from homepage.wsgi import application


def start(args):
    """
    Starts the homepage application server.
    """
    serve(application, host=args.addr, port=args.port)


def migrate(args):
    """
    Runs migrations for the homepage server.
    """
    call_command(
        'migrate',
        fake=args.fake,
        interactive=False,
    )


def createsuperuser(args):
    """
    Creates a superuser.
    """
    from django.contrib.auth.models import User
    User.objects.create_superuser(
        username=args.username,
        email=args.email,
        password=args.password,
    )


def main():
    os.environ['DJANGO_SETTINGS_MODULE'] = 'homepage.settings'

    django.setup()

    parser = argparse.ArgumentParser(description='The Homepage App')

    parser.add_argument('--version', action='version',
                        version=VERSION,
                        help="Print the version number and exit.")

    subparsers = parser.add_subparsers(help="Sub-command help")

    # start
    start_parser = subparsers.add_parser('start', help="Run the app server.")

    start_parser.add_argument('--addr', default='0.0.0.0',
                              help="Optional IP address to bind to")
    start_parser.add_argument('--port', default=8000, type=int,
                              help="Port to bind to")

    # migrate
    start_parser.set_defaults(func=start)

    migrate_parser = subparsers.add_parser('migrate',
                                           help="Migrate the database.")
    migrate_parser.add_argument('--fake', action='store_true',
                                dest='fake', default=False,
                                help='Mark migrations as run without actually '
                                     'running them.')
    migrate_parser.set_defaults(func=migrate)

    # createsuperuser
    createsuperuser_parser = subparsers.add_parser('createsuperuser',
                                                   help="Create a superuser.")

    createsuperuser_parser.add_argument('--username', default='admin',
                                        help="Specifies the username for the"
                                             "superuser.")
    createsuperuser_parser.add_argument('--email', default='admin@example.com',
                                        help="Specifies the email address for "
                                             "the superuser.")
    createsuperuser_parser.add_argument('--password', default='admin',
                                        help="Specifies the password for the "
                                             "superuser.")

    createsuperuser_parser.set_defaults(func=createsuperuser)

    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()
