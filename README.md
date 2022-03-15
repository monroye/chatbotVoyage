## Usage
If you want, you can train the model with the instruction
```sh
   rasa train
   ```
Then, just run the actions-server:
```sh
   rasa run actions
   ```
And finally, in a new terminal, start a conversation
```sh
   rasa shell
   ```
The main files are 

- domain.yml
- data/rules.yml
- data/stories.yml
- actions.actions.yml

A good example about how to manipulate those files and train the model for **Rasa 3.0** can be seen [here (youtube video)](https://www.youtube.com/watch?v=PfYBXidENlg&ab_channel=Rasa). 



