import shutil
import textwrap

def print_status(status):
    terminal_width = shutil.get_terminal_size().columns
    half_width = terminal_width // 2 + 30
    wrapped_text = ""
    
    for line in status["status_message"].splitlines():
        if len(line) <= half_width:
            wrapped_text += line + '\n'
        else:
            wrapped_lines = textwrap.wrap(line, width=half_width)
            wrapped_text += '\n'.join(wrapped_lines) + '\n'
    wrapped_text = wrapped_text[:-1]

    print("-"*half_width)
    print(wrapped_text)
    print("-"*half_width)

    status_link = ""
    for line in status["status_link"].splitlines():
        if len(line) <= half_width:
            status_link += line + '\n'
        else:
            wrapped_lines = textwrap.wrap(line, width=half_width)
            status_link += '\n'.join(wrapped_lines) + '\n'
    status_link = status_link[:-1]

    print(status["status_type"].upper() + " " + status_link)
    print("-"*half_width)
    print(status["author"] + " " + status["status_published"])
    print("-"*half_width)
    print("👍 " + status["num_likes"] + "  😍 " + status["num_loves"] + "  😮 " + status["num_wows"] 
          + "  😂 " + status["num_hahas"] + "  😢 " + status["num_sads"] + "  😡 " + status["num_angrys"] 
          + "  💬 " + status["num_comments"] + "  ➦ " + status["num_shares"])
    print("-"*half_width)
    print("\n\n")