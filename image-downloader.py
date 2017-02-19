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

import io

import hexchat

# Output functions ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FMT_DEFAULT_MESSAGE = "\017[\00302{addon}\017] {message}"
FMT_DEFAULT_ERROR = "\017[\00302{addon}\017] \002\00304ERROR:\017 {message}"

FMT_MESSAGE = FMT_DEFAULT_MESSAGE
FMT_ERROR = FMT_DEFAULT_ERROR

def _message_impl(*objects, sep=" ", fmt=FMT_MESSAGE):
	"""Print message with given format.
	
	The following variables will be replaced in the `fmt` format string:
		`addon` : replaced with `__module_name__`
		`message` : replaced with the formatted `objects` separated by `sep`
	
	Parameters
	----------
	objects : 
		objects to print
	sep : str, optional
		the separator to print between objects
	fmt : str, optional
		format of message to print
	"""
	buf = io.StringIO()
	print(*objects, sep=sep, end="", file=buf)
	print(fmt.format(addon=__module_name__, message=buf.getvalue()))

def message(*objects, sep=" "):
	"""Print message.
	
	Parameters
	----------
	objects : 
		objects to print
	sep : str, optional
		the separator to print between objects
	"""
	_message_impl(*objects, sep=sep, fmt=FMT_MESSAGE)

def error(*objects, sep=" "):
	"""Print error message.
	
	Parameters
	----------
	objects : 
		objects to print
	sep : str, optional
		the separator to print between objects
	"""
	_message_impl(*objects, sep=sep, fmt=FMT_ERROR)

# Script control command ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
CMD_NAME = "IMGDLER"
CMD_HELP = "Get/set options for the {addon} addon. \
See \"/{command} help\" for more info.".format(
	addon=__module_name__,
	command=CMD_NAME)

def on_command(word, word_eol, userdata):
	"""Handle plugin control commands.
	
	`word[0]` should always be the control command used in hexchat to trigger
	this function.
	
	`word[1]` is the desired control function. The remaining items in `word` are
	arguments to the control function named in `word[1]`.
	
	Recognized control functions with their arguments are:
		* help : prints list of recognized control functions.
		* help <func> : prints help about function <func>.
	
	Parameters
	----------
	word : list of str
		`word[0]` should always be the control command.
		`word[1]`, if present, should be the control function name.
		`word[2:]`, if present, should be the control function arguments.
	word_eol : list of str
		`word_eol[2]`, if present, should be the control function arguments.
	userdata :
		not used
	
	Returns
	-------
	int
		`hexchat.EAT_ALL`
	"""
	
	# Get function name.
	function = word[1].casefold() if len(word) > 1 else None
	
	# Help function.
	if function is None or function in [ "help", "--help", "-h" ]:
		# Get function that help is being requested for, if any.
		function = word[2] if len(word) > 2 else None
		args = word[3:] if len(word) > 3 else None
		print_command_help(function=function, args=args)
	
	# Message format function.
	elif function == "msgfmt":
		global FMT_MESSAGE
		# Save existing format.
		fmt = FMT_MESSAGE
		# If there was no format given, reset to default.
		if len(word) > 2:
			FMT_MESSAGE = word_eol[2]
		else:
			FMT_MESSAGE = FMT_DEFAULT_MESSAGE
		# Give the new format a whirl, and if it fails, reset to the old one.
		try:
			message("sample message")
		except Exception as x:
			FMT_MESSAGE = fmt
			error(type(x).__name__ + ":", x)
	
	# Error format function.
	elif function == "errfmt":
		global FMT_ERROR
		# Save existing format.
		fmt = FMT_ERROR
		# If there was no format given, reset to default.
		if len(word) > 2:
			FMT_ERROR = word_eol[2]
		else:
			FMT_ERROR = FMT_DEFAULT_ERROR
		# Give the new format a whirl, and if it fails, reset to the old one.
		try:
			error("sample message")
		except Exception as x:
			FMT_ERROR = fmt
			error(type(x).__name__ + ":", x)
	
	# Unrecognized function.
	else:
		error("unrecognized control function:", function)
	return hexchat.EAT_ALL

HELP_TEXT = \
"""The {addon} addon automatically downloads images linked to in a channel.

The command "/{control_command}" controls the plugin.
To use one of the control functions: "/{control_command} <FUNCTION>".
For help on a specific function:     "/{control_command} help <FUNCTION>".

The functions are:

    HELP        Display this help text
    MSGFMT      Change the format of regular messages
    ERRFMT      Change the format of error messages
""".format(
	addon=__module_name__,
	control_command=CMD_NAME
)

HELP_TEXT_MSGFMT = \
"""Set the format for regular messages printed by the {addon} addon.

Usage: /{control_command} MSGFMT <format string>

<format string> can be any valid Python format string.
There are two special keys:
    {{addon}} : expands to the name of addon ("{addon}")
    {{message}} : expands to the message

You may use Hexchat control codes (like bold and coloring).

If no format string is given, the format is set to the addon default.
""".format(
	addon=__module_name__,
	control_command=CMD_NAME
)

HELP_TEXT_ERRFMT = \
"""Set the format for error messages printed by the {addon} addon.

Usage: /{control_command} ERRFMT <format string>

<format string> can be any valid Python format string.
There are two special keys:
    {{addon}} : expands to the name of addon ("{addon}")
    {{message}} : expands to the error message

You may use Hexchat control codes (like bold and coloring).

If no format string is given, the format is set to the addon default.
""".format(
	addon=__module_name__,
	control_command=CMD_NAME
)

def print_command_help(**kwargs):
	"""Print help info for addon control command.
	
	Parameters
	----------
	function : str, optional
		name of the control function to print help for - if not set, control
		functions are listed
	args : optional
		any additional help arguments
	context : hexchat.context, optional
		the context to print to
	"""
	
	function = kwargs.get("function")
	args = kwargs.get("args")
	context = kwargs.get("context", hexchat)
	
	# Case fold function name for easier comparison.
	if function is not None:
		function = function.casefold()
	
	# General help.
	if function is None:
		if args is not None:
			error("unexpected arguments:", args)
		context.prnt(HELP_TEXT)
	
	# MSGFMT help.
	elif function == "msgfmt":
		if args is not None:
			error("unexpected arguments:", args)
		context.prnt(HELP_TEXT_MSGFMT)
	
	# MSGFMT help.
	elif function == "errfmt":
		if args is not None:
			error("unexpected arguments:", args)
		context.prnt(HELP_TEXT_ERRFMT)
	
	# Unrecognized function.
	else:
		error("unrecognized control function:", function)

hexchat.hook_command(CMD_NAME, on_command, help=CMD_HELP)

# Print a message to confirm that the plugin was successfully loaded ~~~~~~~~~~~
hexchat.prnt("{addon} {version} plugin loaded".format(
	addon=__module_name__,
	version=__module_version__))
