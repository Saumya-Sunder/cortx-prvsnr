#
# Copyright (c) 2020 Seagate Technology LLC and/or its Affiliates
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
# For any questions about this software or licensing,
# please email opensource@seagate.com or cortx-questions@seagate.com.
#

import config
from scripts.factory.server_check import ServerValidations  # noqa: F401
from scripts.factory.network_check import NetworkChecks  # noqa: F401
from scripts.factory.storage_check import StorageValidations  # noqa: F401
from scripts.factory.controller_check import ControllerValidations  # noqa: F401


class Validators():
    '''Validator class :validation of all checks for given request'''

    @staticmethod  # noqa: C901
    def factory_checks(args):
        if args.postcheck:
            check_list = config.FACTORY_POST_CHECK
        elif args.precheck:
            check_list = config.FACTORY_PRE_CHECK
        elif args.swupdate:
            check_list = config.SW_UPDATE_CHECK
        elif args.fwupdate:
            check_list = config.FW_UPDATE_CHECK
        elif args.fwupdate:
            check_list = config.FW_UPDATE_CHECK
        elif args.unboxing:
            check_list = config.UNBOXING_CHECK
        elif args.c:
            check_list = {args.c: config.ALL_CHECKS[args.c]}
        else:
            print("No valid argument is passed")

        if len(check_list.keys()) < 1:
            print("Check is not available for this flag")

        for check, cls in check_list.items():
            res = getattr(globals()[cls], check)()
            if res:
                if res['ret_code']:
                    print(f"{check}: Failed : {res['message']}")
                    print(f"Response: {res}\n")
                else:
                    print(f"{check}: Success : {res['message']}\n")


if __name__ == '__main__':
    import argparse
    import sys
    argParser = argparse.ArgumentParser()
    argParser.add_argument(
              "--precheck", action='store_true',
              help="Factory deployment Pre check validation")
    argParser.add_argument(
              "--postcheck", action='store_true',
              help="Factory deployment Post check validation")
    argParser.add_argument(
              "--swupdate", action='store_true',
              help="Software update check validation")
    argParser.add_argument(
              "--fwupdate", action='store_true',
              help="Firmware update check validation")
    argParser.add_argument(
              "-unboxing", action='store_true',
              help="Unboxing check validation")
    argParser.add_argument(
              "-c", type=str, choices=config.ALL_CHECKS.keys(),
              help="Name of validation to check")
    argParser.set_defaults(func=Validators.factory_checks)
    args = argParser.parse_args()
    args.func(args)
    sys.exit(0)