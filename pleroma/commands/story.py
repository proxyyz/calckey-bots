# commands/story.py
import random
from send_message import send_message

def handle_command(chat_id, auth_token, base_url, author_name):
    default_name = "Anon"  # Default name if there is no display name for them. 
    if author_name.lower() == "": # Got a special user? make them personalized stories. 
        stories = [
            " Woah, you found a secret message, Hai! - Proxy",       
            # Add more personalized stories. 
        ]

        # Choose a random story for Luke (1 to 5)
        story_index = random.randint(0, len(stories) - 1)
        bedtime_story = stories[story_index]
    else:
        # Personalized stories for other users
        stories = [
            "Once upon a time, in the fascinating world of Soapbox Instances, there was a user named {author_name}. {author_name} embarked on an exciting adventure and discovered the wondrous community of this site. In this magical place, they found friendship, joy, and acceptance. They also encountered the charismatic owner, who welcomed them with open arms. Together with the owner and friends, {author_name} had the time of their life, exploring the mysteries of this siteand creating cherished memories.",
"Amidst the wonders of Soapbox Instances, a user named {author_name} uncovered a remarkable community. In this special place, they encountered a coder, whose kindness knew no bounds. The coder, aka the ownerinvited {author_name} to explore this delightfull site, where they found a place of camaraderie and celebration. The adventures they shared with the owner and staff and newfound friends in the whimsical world of this site filled {author_name}'s heart with happiness and gratitude", 
          "Ermmm, What the scallop! - Proxy", 
          "In a realm filled with enchantment called Soapbox Instances, a user named {author_name} stumbled upon a hidden gem known as soapbox instances  In this welcoming sanctuary, they discovered a world of acceptance and warmth. Little did they know that they would soon meet the owner, who would become their companion on a journey of laughter and joy in the magical realm of this site. {author_name} cherished the memories they made with the owner and friends, forever etched in their heart", 
            # Add more personalized stories for other users here, please. qwq
        ]

        # Choose a random story for other users (6 t
        story_index = random.randint(0, len(stories) - 1)
        bedtime_story = stories[story_index].format(author_name=author_name or default_name)  # Use default_name if author_name is empty. 
    # Send the story, qwq. 
    send_message(chat_id, bedtime_story, auth_token, base_url)
