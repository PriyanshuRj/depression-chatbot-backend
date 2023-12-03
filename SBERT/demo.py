from sentence_transformers import SentenceTransformer
from torch import Tensor
import torch

def cos_sim(a: Tensor, b: Tensor):
    """
    Computes the cosine similarity cos_sim(a[i], b[j]) for all i and j.
    :return: Matrix with res[i][j]  = cos_sim(a[i], b[j])
    """
    if not isinstance(a, torch.Tensor):
        a = torch.tensor(a)

    if not isinstance(b, torch.Tensor):
        b = torch.tensor(b)

    if len(a.shape) == 1:
        a = a.unsqueeze(0)

    if len(b.shape) == 1:
        b = b.unsqueeze(0)

    a_norm = torch.nn.functional.normalize(a, p=2, dim=1)
    b_norm = torch.nn.functional.normalize(b, p=2, dim=1)
    return torch.mm(a_norm, b_norm.transpose(0, 1))

model = SentenceTransformer('similarity-LM')

query = "why is anxiety bad for you?"
docs = ['What are the types of depression?', 'about', 'afternoon', 'anxious', 'ask', 'at what age does anxiety peak?', 'can lack of sleep make you feel sad?', 'can low blood sugar cause suicidal thoughts?', 'casual', 'creation', 'death', 'default', 'depressed', 'do we control our thoughts?', 'does oversleeping cause depression?', 'done', 'evening', 'fact-1', 'fact-10', 'fact-11', 'fact-12', 'fact-13', 'fact-14', 'fact-15', 'fact-16', 'fact-17', 'fact-18', 'fact-19', 'fact-2', 'fact-20', 'fact-21', 'fact-22', 'fact-23', 'fact-24', 'fact-25', 'fact-26', 'fact-27', 'fact-28', 'fact-29', 'fact-3', 'fact-30', 'fact-31', 'fact-32', 'fact-5', 'fact-6', 'fact-7', 'fact-8', 'fact-9', 'friends', 'goodbye', 'greeting', 'happy', 'hate-me', 'hate-you', 'help', 'how can we reduce anxiety?', 'how does depression affect the world?', 'how long can anxiety last?', 'how many thoughts a day do we have?', 'i am a victim of bullying', 'i am afraid i will fail again', 'i am afraid to file a case against bullying', 'i am feeling anxious lately.', 'i am feeling stressed lately', 'i am good for nothing!', 'i am good for nothing.', 'i am lonely!', 'i am sad', 'i am stressed out', "i can't do this anymore", 'i feel i have let my parents down', 'i hate losing.', 'i hate myself!', 'i let everyojokne down', 'i think i am ugly!', "i think i'm losing my mind", 'i want a break', 'i want to kill myself', 'i want to leave the cou ntry and run away', 'i will never succeed in life', "i wish i could've been a winner", 'i wish i was better than them', 'i wish to quit', 'is depression a side effect of diabetes?', 'is school a cause of depression?', 'jokes', 'learn-mental-health', 'learn-more', 'location', 'meditation', 'mental-health-fact', 'morning', 'my time has come', 'neutral-response', 'night', 'no one likes me!', 'no-approach', 'no-response', 'not-talking', 'pandora-useful', 'problem', 'repeat', 'sad', 'scared', 'skill', 'sleep', 'something-else', 'stressed', 'stupid', 'suicide', 'thanks', 'understand', 'user-advice', 'user-agree', 'user-meditation', 'what are the causes of depression?', 'what are the stages of anxiety?', 'what are the top causes of depression?', 'what is depression?', 'what is the 3 3 3 rule for anxiety?', 'what is the biological cause of depression?', 'what is the meaning of anxiety and depression?', 'which age group has the highest rate of depression?', 'which country has the highest rate of depression?', 'which country has the lowest rate of depression?', 'which race has the highest rate of depression?', 'why is anxiety bad for you?', 'worthless', 'wrong', 'i am feeling sad', 'i want to die', 'i want to suicide', 'i feel happy', 'i am over joyed', 'i want to eat apple']

def use_model():
    query_emb = model.encode(query)
    doc_emb = model.encode(docs)

    #Compute dot score between query and all document embeddings
    scores = cos_sim(query_emb, doc_emb)[0].cpu().tolist()

    #Combine docs & scores
    doc_score_pairs = list(zip(docs, scores))

    #Sort by decreasing score
    doc_score_pairs = sorted(doc_score_pairs, key=lambda x: x[1], reverse=True)

    #Output passages & scores
    print(doc_score_pairs[0])

if __name__=="__main__":
    use_model()