def multiple_choice_quiz(questions):
    """
    Takes a list of tuples containing quiz questions and answers in the format:
    (question, options, answer)

    Displays each question and its options, prompts the user to select an option,
    and returns the number of correct answers.

    Args:
    - questions (list of tuples): Quiz questions and answers in the format:
      (question, options, answer)

    Returns:
    - score (int): Number of correct answers.
    """

    # Initialize score and question number
    score = 0
    question_number = 1

    # Loop through each question
    for question, options, answer in questions:
        # Display question number and question
        print(f"\nQuestion {question_number}: {question}")

        # Display options
        for i, option in enumerate(options):
            print(f"{i+1}. {option}")

        # Prompt user for answer
        user_answer = input("\nSelect an option (1-4): ")

        # Check if user answer is correct
        if user_answer == str(answer):
            print("Correct!")
            score += 1
        else:
            print(f"Incorrect. The correct answer is {options[answer-1]}.")

        # Increment question number
        question_number += 1

    # Display final score
    print(f"\nYou scored {score} out of {len(questions)}.")

    return score