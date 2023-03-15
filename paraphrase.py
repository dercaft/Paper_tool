import os, sys
from time import sleep
import openai

# use terminal arguments to get the path to the file to be translated
# and the path to the file to be translated into
KEY="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"

def init_gpt():
    openai.api_key = KEY
    openai.proxy = "http://127.0.0.1:7895"
    # max_send=128
    # send_message = paraphrase_relative
def paraphrase_two2one(text1,text2):
    prompt="请结合所给的两个材料，以更加学术化的中文进行学术论文写作，要求与原文不能有连续七个字以上的相同内容，且语序和用语等要与原文有较大不同，可以添加一些细节。可以替换的词汇包括：“预测”-“推理”，“特征图”-“激活图”，“参数”-“权重”。\n"
    suffix="\n请开始润色：\n"
    # suffix=""
    sender=prompt+"材料1：\n"+text1+"材料2：\n"+text2+suffix
    max_token=4000-len(sender*2) if len(sender*2)<3000 else 1000
    response=openai.Completion.create( \
        model="text-davinci-003", \
        prompt=sender, \
        max_tokens=max_token, \
        temperature=0.7, \
        top_p=1, \
        frequency_penalty=0, \
        presence_penalty=0,
        )
    res=str(response["choices"][0].text)
    res=res.replace("请翻译：","").replace("翻译文本","")
    # sleep(2)
    return res

def paraphrase_relative(text):
    prompt="请帮我以更加学术化的中文来润色以下内容，要求语序和用语等要与原文有较大不同，且字数要多于原文。可以添加一些细节。可以替换的词汇包括：“预测”-“推理”，“特征图”-“激活图”，“参数”-“权重”。 "
    suffix="\n请开始润色：\n"
    # suffix=""
    sender=prompt+text+suffix
    max_token=4000-len(sender*2) if len(sender*2)<3000 else 1000

    response=openai.Completion.create( \
        model="text-davinci-003", \
        prompt=sender, \
        max_tokens=max_token, \
        temperature=0.7, \
        top_p=1, \
        frequency_penalty=0, \
        presence_penalty=0,
        )
    res=str(response["choices"][0].text)
    res=res.replace("请翻译：","").replace("翻译文本","")
    # sleep(2)
    return res

if __name__=="__main__":
    if len(sys.argv) != 3:
        print("Usage: python paraphrase.py [file_to_be_paraphrase] [file_to_be_translated_into]")
        exit()
    else:
        file_to_be_translated = sys.argv[1]
        file_to_be_translated_into = sys.argv[2]
    line=""
    openai.api_key = KEY
    max_send=128
    send_message = paraphrase_relative

    rf=open(file_to_be_translated_into, "w")
    # open file_to_be_translated and read its content
    with open(file_to_be_translated, "r") as f:
        lines=f.readlines()
    accu,i="",0

    for i,line in enumerate(lines):
        t=line.replace(" ","").replace("\t","").replace("\n","").replace("%","").replace("&","").replace("#","").replace("$","").replace("_","").replace("{","").replace("}","").replace("~","").replace("^","").replace("\\","").replace("|","").replace("<","").replace(">","").replace('"',"")
        # replace space, tab, newline, %, &, #, $, _, {, }, ~, ^, \, |, <, >, and "
        if len(t)==0: continue        
        sender=line
        text=send_message(sender)
        # if line[0] == '%': text='%'+' '+text
        rf.write(text)        
        print("line {}/{}: {}-{}\t {}... -> {}...".format(i,len(lines), \
                                        len(sender), len(text), \
                                        line[:-1 if len(sender)<20 else 20].replace("\n",""), \
                                        text[:-1 if len(text)<20 else 20].replace("\n","")))
        sender=""

