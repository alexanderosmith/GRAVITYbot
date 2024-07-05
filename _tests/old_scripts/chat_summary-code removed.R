# Conversation 
library(httr)
library(stringr)
#https://rpubs.com/nirmal/setting_chat_gpt_R

chat_api = ""


hey_chatGPT <- function(answer_my_question) {
  chat_GPT_answer <- POST(
    url = "https://api.openai.com/v1/chat/completions",
    add_headers(Authorization = paste("Bearer", chat_api)),
    content_type_json(),
    encode = "json",
    body = list(
      model = "gpt-3.5-turbo-0301",
      messages = list(
        list(
          role = "user",
          content = answer_my_question
        )
      )
    )
  )
  str_trim(content(chat_GPT_answer)$choices[[1]]$message$content)
}

response <- hey_chatGPT("
   We are attempting to summarize comments from Gravity Spy, an online citizen science project for categorizing data from the interferometers at Hanford and Livingston detectors at LIGO.

Can you summarize the main points? 

Seems to be a calibration line at 600 Hz, but very brief, not really a line.
possibly 45 MHz glitch, but only one spike?
thanks ... might have to do a bit of reading on that myself.   
this is so much more interesting than my real job!"
                        
                        )
cat(response)

