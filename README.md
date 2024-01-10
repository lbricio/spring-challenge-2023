# Spring Challenge 2023

<img width="1819" alt="image" src="https://github.com/lbricio/spring-challenge-2023/assets/81334995/ffc8bcf4-873a-4910-a5b0-ae48069165fa">


### Sobre
Minha primeira participação em uma competição do CodinGame, foi bem divertido e foi bem útil para praticar python e alguns conceitos que
ainda não havia tido oportunidade de aplicar antes como BFS e grafos, terminei no top 8% entre 19,283 participantes.


### Estratégias

- um ponto que dificultou bastante é que você não tinha acesso aos blocos como um plano cartesiano, apenas seu índice atual e os vizinhos
desse índice, que não necessariamente seguem alguma ordem, então sempre é necessário fazer uma busca baseada em árvores
- inicialmente tentei limitar o a busca até os recursos mais próximos à base
- adicionei uma nova busca quando o caminho chegasse ao seu destino e durante o processo
fui aprimorando o cálculo de como verificar a rentabilidade em extender o percuso até um rescurso que estava além da pesquisa inicial,
o resultado acabou sendo algo simples: verificar se a distância até esse novo ponto é menor ou igual a distância do primeiro até a base
- o problema da abordagem de limitar a busca é que quando o nível vai subindo o algoritmo gerava caminhos difíceis de controlar, pois abria bastante o leque de possibilidades, por isso que nas próximas abordagens tentei controlar o caminho bloco por bloco para evitar desperdícios

- na abordagem atualizada tentei controlar a geraçao dos caminhos camadas por camada, começando dos blocos vizinhos da base,
e em seguida os vizinhos do vizinhos, sempre marcando os que já haviam sido contabilizados
- uso o primeiro turno para gerar mapas para poder consumir no restante do jogo, aproveitando que o jogo dá 1000ms
de tempo de resposta para o primeiro turno
- gerando um mapa para cada base com a distância das conexões para cada recurso espalhado pelo mapa
- e também cada recurso tinha uma cópia da distância dele até os demais, então ao calcular as rotas sempre levava em conta essas 
listas das conexões entre os pontos do mapa, e também cada recurso tinha uma cópia da distância ate os demais pontos
- acho que a melhor sacada que eu tive foi em vez de fazer cada passo do algoritmo imprimir o que deveria fazer, fazer cada passo adicionar a
uma lista de "pontos para ir" todos os pontos de destino que eu havia calculado para aquele turno e depois de rodar todos os passos algoritmo 
mandar para uma funçao auxiliar de renderização para fazer algumas otimizações no caminho e imprimir bloco por bloco, inclusive a ideia era tentar 
aproveitar parte de uma rota já existente e criar ramos

### Possíveis melhorias:

- geração da rota: à medida que os nodes se afastavam da base ficava mais difícil de calcular um caminho mais otimizado, e muitas vezes meu BFS
gerava blocos desncessários gastando recursos atoa
- algoritmo pacífico: um ponto que observei ao fim da competiçao e que não utilizei: os algoritmos mais agressivos tendiam a ser melhores,
pois você pode causar interferências nas rotas do adversário, em vez disso sempre optava em minerar mais rápido possível os recursos mais próximos
- dificuldade em medir recompensas: muitas vezes meu algoritmo tendia a optar por um recurso que estava mais próximo em vez de percorrer mais para minerar um grupo maior, esse era difícil de resolver porque meu código foi moldado para priorizar justamente o que estava mais próximo
 
