import math


@hell_cmd(pattern="sin ?(.*)")
async def findsin(event):
    input_str = float(event.text[5:])
    output = math.sin(input_str)
    await eor(event, f"**Value of Sin** `{input_str}`==\n`{output}`")


@hell_cmd(pattern="cos ?(.*)")
async def find_cos(event):
    input_str = float(event.text[5:])
    output = math.cos(input_str)
    await eor(event, f"**Value of Cos** `{input_str}`==\n`{output}`")


@hell_cmd(pattern="tan ?(.*)")
async def find_tan(event):
    input_str = float(event.text[5:])
    output = math.tan(input_str)
    await eor(event, f"**Value of Tan** `{input_str}`==\n`{output}`")


@hell_cmd(pattern="cosec ?(.*)")
async def find_csc(event):
    input_str = float(event.text[7:])
    output = mpmath.csc(input_str)
    await eor(event, f"**Value of Cosec** `{input_str}`==\n`{output}`")


@hell_cmd(pattern="sec ?(.*)")
async def find_sec(event):
    input_str = float(event.text[5:])
    output = mpmath.sec(input_str)
    await eor(event, f"**Value of Sec** `{input_str}`==\n`{output}`")


@hell_cmd(pattern="cot ?(.*)")
async def find_cot(event):
    input_str = float(event.text[5:])
    output = mpmath.cot(input_str)
    await eor(event, f"**Value of Cot** `{input_str}`==\n`{output}`")


@hell_cmd(pattern="square ?(.*)")
async def square(event):
    input_str = float(event.text[8:])
    output = input_str * input_str
    await eor(event, f"**Square of** `{input_str}`==\n`{output}`")


@hell_cmd(pattern="cube ?(.*)")
async def cube(event):
    input_str = float(event.text[6:])  
    output = input_str * input_str * input_str
    await eor(event, f"**Cube of** `{input_str}`==\n`{output}`")


CmdHelp("maths").add_command(
  "cube", "<query>", "Gives the cube of given number"
).add_command(
  "square", "<query>", "Gives the square of given number"
).add_command(
  "cot", "<query>", "Gives the cot of given query"
).add_command(
  "sec", "<query>", "Gives the sec of given query"
).add_command(
  "cosec", "<query>", "Gives the cosec of given query"
).add_command(
  "tan", "<query>", "Gives the tan of given query"
).add_command(
  "sin", "<query>", "Gives the sin of given query"
).add_command(
  "cos", "<query>", "Gives the cos of given query"
).add_info(
  "A Plugin On Mathematics."
).add_warning(
  "✅ Harmlesss Module."
).add()
