import openai
import time
import logging
from datetime import datetime



# gets API Key from environment variable OPENAI_API_KEY
client = openai.OpenAI()

assistant_id = "asst_mFPv7IgkEVyA2gNKepi7u4JL"
thread_id = "thread_aOuQi1DAQweVnG6ppo15OWSb"


def newMessage(myMessage,client, thread_id):
    message = myMessage

    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message,
        

    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="please adress the user as KLaus"
    )
    return run.id


def wait_for_run_completion(client, thread_id, run_id, step,sleep_interval=5):
    """

    Waits for a run to complete and prints the elapsed time.:param client: The OpenAI client object.
    :param thread_id: The ID of the thread.
    :param run_id: The ID of the run.
    :param sleep_interval: Time in seconds to wait between checks.
    """
    while True:
        try:
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run_id)
            if run.completed_at:
                elapsed_time = run.completed_at - run.created_at
                formatted_elapsed_time = time.strftime(
                    "%H:%M:%S", time.gmtime(elapsed_time)
                )
                print(f"Run completed in {formatted_elapsed_time}")
                logging.info(f"Run completed in {formatted_elapsed_time}")
                # Get messages here once Run is completed!
                messages = client.beta.threads.messages.list(thread_id=thread_id)
                last_message = messages.data[step]
                response = last_message.content[0].text.value
                print(f"Assistant Response: {response}")
                break
        except Exception as e:
            logging.error(f"An error occurred while retrieving the run: {e}")
            break
        logging.info("Waiting for run to complete...")
        time.sleep(sleep_interval)
i=0
while True:
    print("donner une entrée")
    a = str(input())
    if a != "Fin!":
       i+=1
       try:
           run_id = newMessage(a, client=client, thread_id=thread_id)
           wait_for_run_completion(client=client, thread_id=thread_id, run_id=run_id, step=i)
       except Exception as e:
           print("il y a eu une erreur...")
           print(e)
    else:
        print("c'est fini")
        break
        