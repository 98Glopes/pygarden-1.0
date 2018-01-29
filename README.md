# pygarden-1.0

## Objetivos:

   Criar um sistema supervisório para um vaso de plantas com Flask (linguagem python) para poder estudar suas funcionalidades e integração com outros módulos como a OpenCV. O deploy será realizado em um Raspberry Pi 3 que fará a ponte entre a aplicação web e o mundo fisico.
   
## Scripts:
   
### index.py

   Arquivo que contém a aplicação principal. Este script importa as classes e funções presentes nos arquivos **hardware.py** e **camera.py**
   
### hardware.py

   Classes e funções criadas para que o app possa se comunicar com as IO's do raspberry. Por ora todas as linhas referente aas GPIOs do RPi3 estão desabilitadas com uma '#' para que o script não retorne nenhum errro quando executado em um desktop.
   
### camera.py

   Contém a classe e as funções necessarias para realizar o streaming do video a partir de uma webcam conectada ao RPi3/Desktop. As classes e funções utilizadas para o stream foram retiradas [deste link](https://blog.miguelgrinberg.com/post/flask-video-streaming-revisited). 

### timer.py

   Script desabilitado, em seu lugar será usado a librarie Threading, que sempre que o server inicia ele incia junto uma nova thread para contar o tempo, acionar, ler e gravar os sensores/atuadores no banco de dados
   
## Templates HTML:

   Os templates HTML utilizados para exibir e organizar os dados foram desenhados e editados utilizando o Adobe Fireworks e Dreamweaver.
   
## Funcionamento:

   ![Pagina Inicial](https://github.com/98Glopes/pygarden-1.0/blob/master/templates/index.fw.png)
   
   A pagina inicial funciona basicamente para visualizar as condições do sistema, sendo possivel ver as leituras dos sensores de temperautra, umidade do ar e umidade do solo (estas funcionalidades ainda não foram de fato implementadas) além do estado atual das valvulas de irrigação, sendo possivel ligar ou desligar uma valvula independente do timer. 
   Ao clicar na camera logo a baixo do titulo, o app redireciona o usuário para um pagina que exibe em tempo real as imagens obtidas pela camera.
   
### Adamento do projeto:

   _Features_ já implementadas:
   * Controle das valvulas de irrigação pela pagina web do app;
   * Controle das valvulas pelo timer (ao menos de uma delas até o momento);
   * Streaming de video a partir de que será posicionada sobre o vaso;
   * Camada de javascript para melhorar a interação client/server;
   * Leituras de temperatura e umidade do ar pelo sensor DHT11.
   
   Com o decorrer do projeto novas _features_ serão implementadas entre elas:   
   * Desenvolvimento de um sensor para ler a umidade do solo e sua devida integração com o software;
   * Desenvolvimento do Timer aumentando suas funcionalidades e melhorando seu desempenho;
   * Gravação dos dados obtidos em um banco de dados.
   
### Para um futuro distante:
   
   Para um futuro distante penso implementar um script que a partir das imagens da camera possa identificar os vegetais plantados com Haar Cascades e partir disso quantificar a quantidade de ervas daninhas no vaso
