# X CODER

class color:
	red = '\033[91m'
	green = '\033[92m'
	blue = '\033[94m'
	yellow = '\033[93m'
	magenta = '\033[95m'
	cyan = '\033[96m'
	white = '\033[97m'
	bold = '\033[1m'
	underline = '\033[4m'
	black='\033[30m'

text = f"\n {color.yellow}[{color.white}<{color.red}/{color.white}>{color.yellow}]{color.white} - {color.cyan}BeliX{color.white} Library Version {color.blue}1.0.5 {color.green}Activated\n {color.yellow}[{color.white}<{color.red}/{color.white}>{color.yellow}]{color.white} - {color.red}Copyright (C) {color.blue}2023 {color.white}X CODER\n {color.yellow}[{color.white}<{color.red}/{color.white}>{color.yellow}]{color.white} - {color.cyan}Bale{color.white} Channel : {color.blue}@belix_py\n{color.yellow}{'_' * 46}\n{color.white}"
print(text)