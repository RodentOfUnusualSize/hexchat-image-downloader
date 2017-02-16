# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

__module_name__        = "Image downloader"
__module_version__     = "0.1-alpha1"
__module_description__ = "Automatically download images mentioned in a channel"
__module_author__      = "Saria"

import hexchat

# Script control command ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CMD_NAME = "IMGDLER"
CMD_HELP = "Get/set options for the {script} script. \
See \"/{command} help\" for more info.".format(
	script=__module_name__,
	command=CMD_NAME)

def on_command(word, word_eol, userdata):
	command = word[1].casefold() if len(word) > 1 else None
	if command == "help":
		print_command_help()
	else:
		print_command_help()
	return hexchat.EAT_ALL

def print_command_help(context=None):
	if context is None:
		context = hexchat
	context.prnt("Help pending.")

hexchat.hook_command(CMD_NAME, on_command, help=CMD_HELP)

# Print a message to confirm that the plugin was successfully loaded ~~~~~~~~~~~
hexchat.prnt("{script} {version} plugin loaded".format(
	script=__module_name__,
	version=__module_version__))
