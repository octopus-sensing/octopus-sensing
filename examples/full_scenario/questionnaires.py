from octopus_sensing.questionnaire.opinion_question import OpinionQuestion
from octopus_sensing.questionnaire import Questionnaire


def get_video_questionnaire(name, experiment_id, stimuli_index, title, output_path="output"):
    video_questionnaire = Questionnaire(name,
                                        experiment_id,
                                        stimuli_index,
                                        title,
                                        output_path=output_path)

    emotions = {"Happiness": 4, "Sadness": 6, "Neutral": 5, "Fear": 3, "Anger": 1}
    question_1 = \
        OpinionQuestion("q1",
                        "1- What emotion did you feel the most?",
                        options=emotions,
                        default_answer=5)
    question_2 = \
        OpinionQuestion("q2",
                        "2- How strong was the emotion that you felt? (0=low and 4=high)",
                        options=5,
                        default_answer=2)

    question_3 = \
        OpinionQuestion("q3",
                        "3- Had you seen this film before?",
                        options={"No": 0, "Yes": 1},
                        default_answer=0)
    question_4 = \
        OpinionQuestion("q4",
                        "4- How positive or negative was the emotion that you felt? (Neutral=4)",
                        options=9,
                        default_answer=4)
    question_5 = \
        OpinionQuestion("q5",
                        "5- What was your arousal level: Calm to Excited? (Neutral=4)",
                        options=9,
                        default_answer=4)
    question_6 = \
        OpinionQuestion("q6",
                        "6- Dominance level: Submissive to Dominance (Controlled vs In-controlled)",
                        options=9,
                        default_answer=4)

    video_questionnaire.add_questions([question_1,
                                       question_2,
                                       question_3,
                                       question_4,
                                       question_5,
                                       question_6])
    return video_questionnaire
