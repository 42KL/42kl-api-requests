# API tools for generating visuals

1. exam-sub-status: checks if pisciners subscribed to exam properly.

## EXAM-SUB-STATUS

Compares users subscribed to an exam event and users subscribed to each of
the exam projects set in the exam event. Then, draws a visual of number of
incorrect subs (subscribed to event and not registered for project, or not
subscribed to event and registered for project) vs. correct subs (subscribed
to event and registered for project).

Outputs a SVG infographic file and a JSON data file listing the intra login
for bad subscriptions, project subscriptions and event subscriptions.

### Usage

1. Open a terminal and navigate to the `42kl-api-requests` directory.
2. Check that the `.env` file has been set up.
3. Run `python3 generate-visuals/exam-sub-status.py` and follow the prompts.
4. Outputs are in current directory, named after your inputs for pool year,
pool month, and the exam event selected.

