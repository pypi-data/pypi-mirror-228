from tketool.lmc.models import *
from tketool.lmc.tasks.task_init import get_init_llm
from tketool.logs import log, print_dash_line


def translate(lang: str, ori_text: str, tllm=None):
    """
    LLMC - translate the str
    lang : the target language
    ori_text : the content text
    """
    if tllm is None:
        tllm = get_init_llm()
    link_model = lmc_linked_model(tllm).set_prompt_template("you are a great translator. \n"
                                                           "please translate the paragraph to {lang} \n"
                                                           "the paragraph is ‘{content}’")

    results, _ = link_model(lang=lang, content=ori_text)

    if len(results)==0:
        log("can't translate the paragraph.")
    else:
        log(f"{ori_text} => {lang}")
        print_dash_line()
        log(results[0])

    return results
