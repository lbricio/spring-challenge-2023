# Spring Challenge 2023

<img width="1440" alt="image" src="https://github.com/lbricio/spring-challenge-2023/assets/81334995/4b63fb87-18e0-4e3d-b9ac-d13565050e8e">

## sobre
Primeira participação em uma competição do CodinGame, foi bem divertido e foi bem útil para praticar Python e alguns conceitos que
ainda não havia conseguido aplicar antes como BFS e grafos, terminei no top 30% entre 5500 participantes.

## estratégias utilizadas

- um ponto que dificultou bastante é que você não tinha acesso aos blocos como um plano cartesiano, apenas seu índece atual e os vizinhos
desse índece, que não necessariamente seguem alguma ordem, então sempre é necessário fazer uma busca baseada em trees
- inicialmente tentei limitar o a busca até os recursos mais próximos à base
- adicionei uma nova busca quando o caminho chegasse ao seu destino e durante o processo
fui aprimorando o cálculo de como verificar se valeria a pena extender o percuso até um rescurso que estava além da pesquisa inicial,
o resultado acabou sendo algo simples: verificar se a distância até esse novo ponto é menor ou igual a distância inicial até a base
- o problema dessa abordagem de limitar a busca é que quando o nível ia subindo o algoritmo gerava caminhos completamente aleatórios,
por isso que nas minhas próximas abordagens tentei controla o caminho bloco por bloco para evitar desperdícios

- a minha abordagem mais atualizada eu tentei controlar a geraçao dos caminhos camadas por camada, começando dos blocos vizinhos da base,
e em seguida vizinho por vizinho
- no primeiro turno uso para gerar mapas para poder consumir no restante do jogo:
- gerando um mapa para cada base com a distância das conexões para cada recurso espalhado pelo mapa
- e também cada recurso tinha uma cópia da distância dele até os demais
- então quando eu estava calculando as rotas sempre levava em conta essa lista de conexões entre os pontos do mapa
- o melhor habilitador foi em vez de fazer cada passo do algoritmo imprimir o que deveria fazer, fazer cada passo adicionar à
lista o seu ponto de destino e depois de rodar todos os passos mandar para uma funçao auxiliar para fazer algumas otimizações no caminho,
inclusive tentar aproveitar parte de uma rota já existente em outra

## pontos a melhorar:

- geração da rota: à medida que os nodes se afastavam da base ficava mais difícil de calcular um caminho mais otimizado, e muitas vezes meu BFS
gerava blocos desncessários gastando recursos atoa
- algoritmo pacífico: um ponto que observei ao fim da competiçao e que não utilizei era que os algoritmos mais agressivos tendiam a ser melhores,
pois você pode quebrar causar interferências nas rotas do adversário
- dificuldade de trabalhar com grupos: muitas vezes meu algoritmo tendia a optar por um recurso que estava mais próximo em vez de percorrer mais para minerar um grupo maior, esse era difícil de resolver porque meu código foi moldado para priorizar justamente o que estava mais próximo
 
