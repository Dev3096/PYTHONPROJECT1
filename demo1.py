def pallindrome(s):
    """
    Check if a string is a palindrome.

    A palindrome reads the same forwards and backwards, ignoring spaces, punctuation, and case.

    :param s: The string to check.
    :return: True if the string is a palindrome, False otherwise.
    """
    # Normalize the string by removing spaces and converting to lowercase
    normalized_str = ''.join(c.lower() for c in s if c.isalnum())
    # Check if the normalized string is equal to its reverse
    return normalized_str == normalized_str[::-1]