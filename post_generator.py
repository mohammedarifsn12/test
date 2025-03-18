from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()

def get_length_str(length):
    if length == "Short":
        return "1 to 5 lines"
    if length == "Medium":
        return "6 to 10 lines"
    if length == "Long":
        return "11 to 15 lines"

def generate_hashtags(post_content):
    """Generate relevant hashtags using LLM based on the post content."""
    prompt = f"""
    Generate relevant LinkedIn hashtags based on the following post.
    1. Return exactly 4-6 hashtags.
    2. Use short and common hashtags related to the topic.
    3. Output format should be a single line of space-separated hashtags.

    Post:
    {post_content}

    Hashtags:
    """
    response = llm.invoke(prompt)
    return response.content.strip()

def generate_post(length, language, tag):
    """Generate a LinkedIn post and append relevant hashtags."""
    prompt = get_prompt(length, language, tag)
    response = llm.invoke(prompt)
    post_content = response.content.strip()
    
    hashtags = generate_hashtags(post_content)
    final_post = f"{post_content}\n\n{hashtags}"  # Append hashtags
    return final_post

def get_prompt(length, language, tag):
    length_str = get_length_str(length)

    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    If Language is Hinglish then it means it is a mix of Hindi and English. 
    The script for the generated post should always be English.
    '''
    
    examples = few_shot.get_filtered_posts(length, language, tag)

    if len(examples) > 0:
        prompt += "4) Use the writing style as per the following examples."

    for i, post in enumerate(examples):
        post_text = post['text']
        prompt += f'\n\n Example {i+1}: \n\n {post_text}'

        if i == 1: # Use max two samples
            break

    return prompt

if __name__ == "__main__":
    print(generate_post("Medium", "English", "Mental Health"))
