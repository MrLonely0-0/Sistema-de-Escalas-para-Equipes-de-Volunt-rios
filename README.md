# Sistema de Escalas para Equipes de Voluntários

Relatório técnico detalhado para um sistema de gestão de escalas e equipes de voluntários, cobrindo arquitetura, modelagem, algoritmos, fluxos, notificações, API, infraestrutura, testes, monitoramento, fases e segurança.

## 1. Arquitetura do Sistema

- **Backend:** Django (Python) ou NestJS (Node.js) sobre REST ou GraphQL; autenticação JWT com refresh tokens e suporte OAuth2 social; Redis para cache/fila; Celery (Django) ou Bull (Nest) para jobs.
- **Banco de Dados:** PostgreSQL como fonte de verdade; Redis para cache de leitura e filas; usar UUIDs como PK.
- **Frontend:** React + TypeScript ou Vue + TypeScript; estado com React Query/RTK Query ou Pinia; UI kit Material UI ou Ant Design.
- **Mobile:** React Native ou Flutter; uso das mesmas APIs.
- **Infra:** Contêineres Docker; orquestração via docker-compose no dev e ECS/Kubernetes em produção; armazenamento de arquivos em S3/GCS; CDN opcional para ativos públicos.
- **Observabilidade:** logs estruturados, métricas (Prometheus/OpenTelemetry), tracing distribuído (OTel).

## 2. Modelagem de Dados (PostgreSQL)

Entidades principais com chaves UUID e colunas `created_at`/`updated_at` (triggers ou ORM). Campos JSONB permitem flexibilidade controlada. Principais relações:

- `users`: identidade, contato, tipo (`admin`, `volunteer`), verificação de e-mail/telefone.
- `teams`: metadados da equipe, `admin_id`, `code` e `invite_link_token` para convites, `settings` em JSONB.
- `team_members`: relação M:N usuário-equipe com `role` (volunteer/admin) e `status` (`pending`, `active`, `inactive`).
- `roles`: funções/cargos por equipe, permissões em JSONB e `color` opcional.
- `volunteer_roles`: M:N voluntário-função com `proficiency_level`.
- `availability`: disponibilidade por data ou recorrente (`day_of_week`, `recurrence_pattern`), horário e `is_recurring`.
- `regular_schedules`: escalas padrão (dia da semana, horário, `required_roles`, `frequency`).
- `events`: eventos pontuais com `required_roles`, urgência e status (`draft`, `published`, `cancelled`).
- `schedule_content`: anexos/partituras/leituras associados a uma escala regular ou evento.
- `generated_schedules`: guarda a escala mensal (`schedule_data` JSONB), `generation_algorithm`, status (`draft`, `published`, `archived`).
- `assignments`: atribuições individuais com `schedule_date`, `role_id`, status (`assigned`, `confirmed`, `cancelled`, `replaced`).
- `assignment_history`: trilha de auditoria por atribuição.
- `notifications` e `notification_preferences`: controle de notificações e canais (email, whatsapp, push, in_app).

### Observações de integridade

- Índices compostos para buscas frequentes: `(team_id, month, year)` em `generated_schedules`, `(schedule_date, user_id)` em `assignments`.
- Restrições de unicidade: `UNIQUE(user_id, team_id)` em `team_members`; `UNIQUE(team_id, month, year)` em `generated_schedules`.
- `CHECK` para `day_of_week` (0-6) e enums; em ORMs, use `ChoiceField` ou `Enum` tipados.

## 3. Algoritmo de Geração de Escalas

### Passos principais

1. Coleta: voluntários disponíveis, escalas regulares ativas, eventos publicados, histórico recente (12 semanas) e contadores mensais.
2. Inicialização: cria estrutura `{month, year, assignments, statistics}`.
3. Alocação de escalas regulares: para cada data prevista, filtra candidatos por função, disponibilidade e conflitos; ordena por menos escalas no mês, última escala mais antiga e `priority_score` (disponibilidade explícita > recorrente > não declarada).
4. Alocação de eventos: mesma lógica, permitindo `is_urgent` priorizar disponibilidade imediata.
5. Balanceamento: detecta desequilíbrios (limite por voluntário/função) e reatribui se necessário.
6. Validação: checa lacunas de funções, conflitos de horário e limites de descanso mínimo.

### Regras de negócio

- Disponibilidade específica tem prioridade sobre recorrente; ausência de disponibilidade é último recurso.
- Rodízio considera histórico de 12 semanas e mínimo de dias de descanso entre escalas (parametrizável).
- Limite de escalas/mês por voluntário e distribuição equitativa entre funções; respeita preferências de horário.
- Eventos de última hora usam caminho rápido: filtro de disponibilidade imediata, notificação prioritária e possibilidade de substituição automática.

## 4. Fluxos de Trabalho

### Cadastro e convite

1. Admin cria equipe → gera `code` e `invite_link_token`.
2. Admin busca usuários existentes, envia convite (e-mail/whatsapp) ou compartilha link/código; gerencia pendentes.
3. Voluntário recebe convite → aceita/recusa; se aceitar, cria conta (se novo), configura perfil, disponibilidade e funções; admin é notificado.

### Geração e aprovação de escala

1. Admin inicia geração mensal.
2. Sistema coleta disponibilidades, escalas regulares, eventos e histórico.
3. Executa algoritmo e exibe proposta.
4. Admin aprova, ajusta manualmente ou reprocessa com parâmetros.
5. Ao aprovar: persiste em `generated_schedules`, cria `assignments`, dispara notificações e agenda lembretes (24h antes e no dia).

## 5. Notificações

- Templates tipados por canal (email, whatsapp, push) e variáveis (ex.: `volunteerName`, `date`, `time`, `role`).
- Serviço envia em paralelo respeitando preferências e verificação de telefone para WhatsApp; lembretes agendados via scheduler (Celery beat ou equivalente).
- Status em `notifications`: `pending`, `sent`, `failed`, `read`; jobs de retry para falhas transitórias.

## 6. API Endpoints (sugestão)

- **Auth/Usuários:** POST `/api/auth/register|login|refresh|forgot-password|reset-password`; GET/PUT `/api/users/me`; GET `/api/users/search?q=`.
- **Equipes:** CRUD `/api/teams`; convites `/api/teams/:id/invite` e `/api/teams/join/:code`; membros `/api/teams/:id/members` (GET/PUT/DELETE).
- **Funções:** CRUD `/api/teams/:teamId/roles`; GET/PUT/DELETE `/api/roles/:id`; POST/GET `/api/users/me/roles`.
- **Disponibilidade:** CRUD `/api/availability`; overview `/api/teams/:teamId/availability/overview`.
- **Escalas/Eventos:** CRUD `/api/teams/:teamId/regular-schedules` e `/api/teams/:teamId/events`; conteúdo `/api/schedules/:id/content`.
- **Geração:** POST `/api/teams/:teamId/schedules/generate`; GET `/api/teams/:teamId/schedules/:month/:year`; PUT `/api/schedules/:id`; POST `/api/schedules/:id/publish`; GET `/api/assignments/upcoming`; POST `/api/assignments/:id/confirm|cancel`.
- **Notificações:** GET `/api/notifications`; PUT `/api/notifications/:id/read`; GET/PUT `/api/notification-preferences`.

## 7. Infra e Ambiente de Desenvolvimento

- `docker-compose` com serviços: `postgres`, `redis`, `backend`, `frontend`, `celery`, `celery-beat`; volumes para dados do Postgres.
- Variáveis de ambiente: `DATABASE_URL`, `REDIS_URL`, segredos (JWT, OAuth, SMTP), `STORAGE_BUCKET`.
- Script inicial: instalar dependências (`npm install`, `pip install -r requirements.txt`), copiar `.env.example`, migrar DB, criar superusuário, subir compose.
- CI/CD: lint + testes (unit/integration) + migrations check; build de imagens; deploy em staging/produção com migrações automatizadas.

## 8. Testes Automatizados

- **Unitários:** lógica de disponibilidade, ordenação de candidatos, limites de rodízio, notificações (mock de serviços externos).
- **Integração:** fluxo de geração completo gravando em DB; envio de notificação criando registro `notifications` e agendando lembretes; confirmação/cancelamento de atribuições.
- **Contratos/API:** schemas OpenAPI/Swagger ou Pact para clientes web/mobile.
- **E2E (opcional):** Cypress/Playwright cobrindo geração e aprovação de escala.

## 9. Monitoramento e Logs

- Métricas: tempo de geração, taxa de sucesso de notificações, confirmações, uso horário, falhas de jobs, filas.
- Logs estruturados JSON com `service`, `team_id`, `month`, `year`, `duration_ms`, `volunteers_count`, `assignments_generated`, `algorithm_version`, `warnings`.
- Alertas: falha de envio > limiar, geração acima de SLA, backlog de fila.

## 10. Plano de Implementação por Fases

- **Fase 1 (MVP - 4 semanas):** autenticação, usuários, equipes/membros, funções, disponibilidade básica, CRUD de escalas regulares e eventos.
- **Fase 2 (Geração - 3 semanas):** algoritmo básico, UI de aprovação, notificações por e-mail, confirmação de presença.
- **Fase 3 (Otimização - 2 semanas):** rodízio avançado, WhatsApp, app mobile básico, substituição automatizada.
- **Fase 4 (Refinamento - 2 semanas):** dashboard de analytics, templates customizáveis, API pública, documentação completa.

## 11. Recursos e Custos

- Equipe: 1 backend sênior (Python/Node), 1 frontend sênior (React), 1 mobile (React Native), 1 designer UI/UX, 1 DevOps/Infra.
- Custos mensais estimados: cloud $200–500, terceiros (Twilio/SendGrid) $50–200, monitoramento $50–100. Total $300–800/mês (estimado, variar por uso).

## 12. Segurança e Conformidade

- JWT com refresh, rate limiting em endpoints sensíveis, validação de input, hashing de senhas (Argon2/BCrypt), criptografia de dados sensíveis em repouso e trânsito.
- Auditoria para ações administrativas (ex.: mudanças em `assignments`, `roles`, `teams`).
- Backups diários e testes de restauração; política de retenção.
- LGPD/GDPR: consentimento para notificações, opt-out, exclusão de dados, minimização de coleta.

## 13. Documentação para Usuários

- **Administrador:** criar/gerir equipes, configurar funções, gerar/aprovar escalas, gerir membros, ajustes de notificações e preferências.
- **Voluntário:** configurar perfil, marcar disponibilidade, selecionar funções, confirmar/cancelar escalas, definir preferências de notificação.