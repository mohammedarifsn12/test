from llm_helper import llm
from few_shot import FewShotPosts

few_shot = FewShotPosts()

def get_length_str(length):
    """Convert length choice to human-readable format."""
    return {
        "Short": "1 to 5 lines",
        "Medium": "6 to 10 lines",
        "Long": "11 to 15 lines"
    }.get(length, "6 to 10 lines")

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

def generate_post(length, language, tag, user_templates=None):
    """Generate a LinkedIn post using user-provided templates if available."""
    if user_templates and len(user_templates) >= 2:
        prompt = get_prompt_from_templates(user_templates, length, language, tag)
    else:
        prompt = get_prompt(length, language, tag)  # Fall back to pre-built templates
    
    response = llm.invoke(prompt)
    post_content = response.content.strip()
    
    hashtags = generate_hashtags(post_content)
    return f"{post_content}\n\n{hashtags}"

def get_prompt_from_templates(templates, length, language, tag):
    """Create a prompt using multiple user-provided templates."""
    length_str = get_length_str(length)
    
    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    If Language is Hinglish, it is a mix of Hindi and English (script should be English).
    
    Use the following examples as writing style references:
    '''
    
    # Include up to 3 examples from user templates
    for i, post in enumerate(templates[:3]):  
        post_text = post.get('text', 'No example text provided.')
        prompt += f'\n\nExample {i+1}: \n\n {post_text}'

    return prompt

def get_prompt(length, language, tag):
    """Generate a LinkedIn post prompt using pre-built examples."""
    length_str = get_length_str(length)

    prompt = f'''
    Generate a LinkedIn post using the below information. No preamble.

    1) Topic: {tag}
    2) Length: {length_str}
    3) Language: {language}
    If Language is Hinglish, it is a mix of Hindi and English (script should be English).
    '''
    
    examples = few_shot.get_filtered_posts(length, language, tag)

    if examples:
        prompt += "4) Use the writing style as per the following examples."

    for i, post in enumerate(examples[:2]):  # Use up to 2 pre-built samples
        post_text = post['text']
        prompt += f'\n\nExample {i+1}: \n\n {post_text}'

    return prompt

if __name__ == "__main__":
    print(generate_post("Medium", "English", "AI and Ethics"))
