# Natural Language First Project
First Project for 2019-2020 Natural Language Course in Instituto Superior Técnico.


The goal was to build a retrieval-based chatbot using a set of FAQs.
Being given a user request, the chatbot should find the most “similar question” from its knowledge base and return the ID of its answer. As an example, being given a
list of user requests, in which the user request in line 56 is:

>Demora quanto tempo para emitir um certificado de admissibilidade?

and considering that in the KB.xml you have:

 ```html
<questions>
  <question>Em que prazo é emitido um certificado de admissibilidade?</question>
  <question>Quanto demora a ser emitido um certificado de admissibilidade?</question>
  <question>O certificado de admissibilidade é emitido em quanto tempo?</question>
  <question>Em quantos dias é emitido um certificado de admissibilidade?</question>
</questions>

<answer id = "145">
  O prazo previsto na Lei é de 10 dias, mas, em regra, os certificados são emitidos entre três a cinco
  dias úteis.
</answer>
  ```
Your system should return ***in line 56***:
145
