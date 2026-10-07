# Visão geral do Nexus (2026-10-07)

## O quê e por quê

O Nexus é uma rede social de micro-posts no estilo Twitter, construída como
Atividade Prática 1 da disciplina Desenvolvimento de Software Apoiado por IA
(UFPA, 2026.4). O objetivo da aplicação é permitir que usuários publiquem
mensagens curtas (posts), sigam uns aos outros e interajam com o conteúdo,
formando um feed cronológico personalizado.

O projeto é conduzido em Specification-Driven Development: cada parte do
sistema tem uma spec datada, escrita antes do código que a implementa, e
commitada antes dele. As decisões de escopo privilegiam um produto funcional
e demonstrável ao vivo em uma URL pública, sobre volume de código.

## Escopo (em ordem de prioridade para a apresentação)

1. **Autenticação abstraída** — login por username, sem senha complexa, para
   viabilizar a demonstração. Cadastro mínimo (username + display name).
2. **Perfil de usuário** — exibir bio, avatar e lista de posts de um usuário;
   permitir editar o próprio perfil.
3. **Posts** — criar, listar, editar e apagar posts de texto (limite de 280
   caracteres) com suporte opcional a uma imagem.
4. **Feed** — duas visões: feed global (todos os posts, ordem cronológica
   reversa) e feed pessoal (apenas de quem o usuário segue).
5. **Follow/Unfollow** — seguir e deixar de seguir outros usuários; exibir
   contadores de seguidores e seguindo.
6. **Likes e comentários (replies)** — curtir posts e responder a posts.
7. **Moderação via Django admin** — usar o admin nativo do Django para
   remover posts, banir usuários e inspecionar denúncias simples.

## Fora do escopo

- Mensagens diretas (DM).
- Notificações em tempo real.
- Trending topics e busca avançada.
- Reposts.
- OAuth com provedores externos (Google, GitHub etc.).
- Aplicativo mobile nativo.
- Recuperação de senha, 2FA, verificação por e-mail.
- Algoritmo de recomendação — o feed é estritamente cronológico.

## Critérios de aceitação de alto nível

- Um usuário consegue se cadastrar, fazer login, criar um post, seguir outro
  usuário, curtir e comentar um post.
- O feed pessoal mostra apenas posts de contas seguidas.
- O admin do Django permite remover um post e banir um usuário.
- A aplicação está publicada em URL pública e abre com um clique.
- Cada parte do sistema listada em "Escopo" tem uma spec própria, datada em
  `SPEC/`, commitada antes do código correspondente.

## Restrições conhecidas

- O desenvolvimento usa modelos de IA gratuitos (Qwen 3 27B via Groq no
  Cline), com limite de tokens. Isso reduz a ambição de volume de código e
  prioriza clareza sobre esperteza algorítmica.
- Não há meta de atingir 100 mil linhas de código (cloc). O número real será
  publicado no README com transparência.