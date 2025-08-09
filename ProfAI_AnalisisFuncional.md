# ProfAI – Análisis Funcional (MVP + Extensiones)

## 1. Visión
ProfAI es un profesor de IA estilo MIT con inteligencia emocional y capacidades de voz que entrega aprendizaje especializado y adaptativo en tiempo real. Objetivo: acelerar la transición de un aprendiz (junior/mid) a un builder capaz de diseñar, prototipar y desplegar soluciones basadas en LLMs, dominando tanto teoría rigurosa como "vibe coding" con herramientas modernas.

## 2. Alcance Inicial (MVP)
- Especialización elegida: **Hybrid (Teoría MIT-style + Aplicación inmediata con "vibe coding")**.
- Formato elegido: **Lecciones cortas diarias (micro-learning) + Deep Dive semanal + Video tutorials con screen capture**.
- Modalidad emocional: **Detección textual de frustración/confusión (fase 1)** + voice tone analysis como extensión.
- Modalidad de interacción: **Text-first** con voz como extensión progresiva (STT/TTS).
- Integración comunitaria: **Hack-Nation channels** para discusión peer-to-peer.

## 3. Actores

| Actor | Descripción | Objetivos |
|-------|-------------|-----------|
| Aprendiz | Usuario final (dev, estudiante, autodidacta) | Aprender rápido, feedback inmediato, mantenerse actualizado |
| Motor de Tutoría (Agente Principal) | Orquestador pedagógico con estilo MIT | Generar explicaciones rigurosas pero accesibles, rutas dinámicas |
| Agente de Evaluación | Analiza desempeño / errores | Calificar, detectar brechas, evaluar vibe coding |
| Agente de Actualización de Contenido | Escanea fuentes externas en tiempo real | Inyectar novedades (tools, papers, framework updates) |
| Agente Emocional | Clasifica tono / señales multimodales | Ajustar pedagogía, detectar frustración |
| Agente de Video | Genera screen captures y tutorials | Crear contenido visual para "vibe coding" |
| Agente Comunitario | Integración Hack-Nation channels | Facilitar peer discussion, compartir insights |
| Admin / Curador | (Opcional) Revisa calidad | Aprobar contenido crítico |

## 4. Casos de Uso (Resumen - Expandido)

| ID | Caso | Actor Primario | Desencadenante | Resultado |
|----|------|----------------|----------------|-----------|
| CU-01 | Iniciar sesión / Perfil de Aprendiz | Aprendiz | Primera visita | Perfil creado con nivel estimado |
| CU-02 | Diagnóstico inicial | Motor Tutoría | CU-01 | Mapa de competencias |
| CU-03 | Lección diaria personalizada | Aprendiz | Apertura diaria | Entrega micro-lección + mini quiz |
| CU-04 | Explicación alternativa ("No entiendo") | Aprendiz | Frustración detectada | Nueva explicación con analogía MIT-style |
| CU-05 | Sugerencia de práctica aplicada | Motor Tutoría | Fin de lección | Ejercicio + code scaffold |
| CU-06 | Evaluación de ejercicio | Agente Evaluación | Envío solución | Feedback inmediato estructurado |
| CU-07 | Actualización de contenido | Agente Actualización | Cron / Evento | Nueva lección en backlog |
| CU-08 | Detener sobrecarga cognitiva | Agente Emocional | Señal de frustración | Recomienda pausa / simplifica |
| CU-09 | Deep Dive semanal | Aprendiz | Día programado | Sesión extendida integradora |
| CU-10 | Progreso y Próximos Pasos | Aprendiz | Solicitud / Hito | Dashboard adaptativo |
| **CU-11** | **Interacción por voz** | **Aprendiz** | **Comando voz / preferencia** | **Respuesta TTS + comprensión STT** |
| **CU-12** | **"Vibe coding" en tiempo real** | **Aprendiz** | **Solicitud experimentar** | **Replit/Codespaces + live coding** |
| **CU-13** | **Video tutorial con screen capture** | **Agente Video** | **Lección práctica** | **Video paso-a-paso generado** |
| **CU-14** | **Compartir en Hack-Nation** | **Agente Comunitario** | **Logro significativo** | **Post automático en channels** |
| **CU-15** | **Actualización automática trending** | **Agente Actualización** | **Nuevas herramientas IA** | **"What's New" lesson auto-generada** |

## 5. User Stories (MVP + Extensiones)

1. Como aprendiz quiero un diagnóstico inicial para enfocar mis esfuerzos.
2. Como aprendiz quiero micro-lecciones de <5 min para progresar diariamente.
3. Como aprendiz quiero pedir "explícalo diferente" y recibir analogía concreta estilo MIT.
4. Como aprendiz quiero ver código ejecutable inmediato tras la teoría.
5. Como aprendiz quiero feedback automático en segundos al subir mi solución.
6. Como aprendiz quiero saber si estoy bloqueado y recibir una sugerencia de pausa.
7. Como sistema quiero actualizar mi base de lecciones con nuevos frameworks semanalmente.
8. Como aprendiz quiero un resumen semanal de progreso y lagunas.
9. Como aprendiz quiero hablar con el profesor y escuchar explicaciones (voice mode).
10. Como aprendiz quiero hacer "vibe coding" experimental con herramientas reales.
11. Como aprendiz quiero video tutorials generados automáticamente con screen capture.
12. Como aprendiz quiero compartir mis logros con la comunidad Hack-Nation.
13. Como aprendiz quiero ser notificado de nuevas herramientas IA trending.
14. Como profesor quiero generar contenido actualizado automáticamente de fuentes oficiales.

## 6. Requisitos Funcionales (RF - Expandido)

| ID | Requisito |
|----|-----------|
| RF-01 | Sistema debe generar evaluación diagnóstica inicial (quiz adaptativo + auto-reporte). |
| RF-02 | Motor debe seleccionar diariamente una lección basada en lagunas y spaced repetition. |
| RF-03 | Cada lección debe incluir: objetivo, explicación breve, ejemplo aplicado, mini quiz. |
| RF-04 | Usuario puede solicitar reformulación (simplificar / analogía / paso a paso / más técnico). |
| RF-05 | Sistema detecta frustración por patrones lingüísticos y ajusta nivel. |
| RF-06 | Ejercicios prácticos generan scaffold (prompt + snippet) y criterios de evaluación. |
| RF-07 | Feedback estructurado: Correctitud, Eficiencia, Claridad, Próximo Paso. |
| RF-08 | Registro persistente de desempeño (vector + metadatos temporales). |
| RF-09 | Dashboard de progreso (competencias, retención, consistencia). |
| RF-10 | Ingesta automática semanal de novedades (fuentes: repos docs / RSS / arXiv). |
| **RF-11** | **Interfaz de voz bidireccional (STT para input, TTS para output).** |
| **RF-12** | **Integración con Replit API y GitHub Codespaces para "vibe coding" en tiempo real.** |
| **RF-13** | **Generación automática de video tutorials con screen capture.** |
| **RF-14** | **Integración con Hack-Nation channels para compartir logros y discusión.** |
| **RF-15** | **Pipeline automático de "What's New" lessons basado en trending tools.** |
| **RF-16** | **Detección de tono emocional en voz (extensión fase 2).** |
| **RF-17** | **Sistema de templates para diferentes estilos pedagógicos (MIT riguroso vs casual).** |

## 7. Requisitos No Funcionales (RNF)
| Categoría | RNF |
|-----------|-----|
| Rendimiento | Respuesta < 3s para reformulaciones; feedback ejercicios < 10s (cola asíncrona). |
| Escalabilidad | Multi-tenant; soporte > 5k usuarios concurrentes (colasar tareas batch). |
| Observabilidad | Logs estructurados + métricas: latencia, tasa reformulación, abandono. |
| Privacidad | No almacenar datos sensibles; opción borrar perfil. |
| Ética | Explicaciones transparentes (mostrar fuentes / disclaimers). |
| Disponibilidad | 99% uptime MVP. |
| Evolutividad | Arquitectura modular de agentes (plug-in). |

## 8. Modelo de Competencias
Dominios: Fundamentos ML, LLM Ops, Prompt Engineering, Evaluación, Integraciones API, Deployment ligero.
Cada competencia: nivel (0-5), confianza, última práctica, caducidad (decay). Vector usado para recomendación.

## 9. Arquitectura Lógica (Capas)
- Capa Interacción: Web (Next.js / SvelteKit) + API conversacional.
- Capa Orquestación: Scheduler + Router Pedagógico + Policy Layer.
- Capa Agentes:
  - Tutor (plan, explicación, reformulación)
  - Evaluador (grading rubric + code analysis / test snippets)
  - Actualizador (scraper + resumidor + curator rules)
  - Emocional (clasificador sentimiento / confusión)
- Capa Datos: Store de usuarios (perfil, progreso), Vector Store (lecciones, embeddings), Metadata (historial).
- Capa Modelo: LLM principal (GPT-4o u otro), modelos ligeros (sentiment), embeddings (text-embedding-3-small o similar).

## 10. Diseño del Agente Principal (Tutor)
Flujo:
1. Entrada (usuario + contexto sesión + estado emocional + vector gaps)
2. Policy: ¿Continuar tema? ¿Introducir repaso? ¿Reducir dificultad?
3. Generación Lesson Plan (estructura JSON controlada)
4. Ensamblado (plantilla + contenido base + fuentes)
5. Entrega + Instrumentación (tracking)
6. Bucle: Monitoreo señales -> Reinstrucción / Reformulación

Outputs formateados (contratos JSON):
- lesson_plan: objetivos[], prereqs[], secuencias[]
- exercise: prompt, scaffold_code, evaluation_rubric
- feedback: scores{}, recommendations[]

## 11. Detección Emocional (Fase 1)
- Input: Texto del usuario (últimos N turnos)
- Features: léxicos de frustración, métricas (tiempo respuesta, frecuencia "no entiendo")
- Clasificador: Regla híbrida + modelo sentiment (zero-shot)
- Acción: Ajustar dificultad / ofrecer opción: "Ver ejemplo paso a paso" / pausa.

## 12. Fuentes de Contenido / Ingesta
- Cron semanal: crawler (docs LangChain / Hugging Face / Vercel AI SDK / ArXiv tópicos ML)
- Pipeline: Fetch -> Extract -> Chunk -> Embed -> Index -> Curate (umbrales calidad) -> Backlog

## 13. Datos Persistentes
| Tipo | Ejemplo | Almacenamiento |
|------|---------|----------------|
| Perfil Usuario | nivel_estimado, preferencias_formato | DB relacional/kv |
| Historial | turns conversacionales | Store paginado |
| Vector Lecciones | embedding, tags, dificultad | Vector DB |
| Evaluaciones | resultado_quiz, rubric_scores | DB |
| Telemetría | reformulation_rate, frustration_events | Time-series |

## 14. Evaluación Continua
Métricas Pedagógicas:
- Learning Velocity = (competencias_suben / tiempo)
- Retention Score (spaced intervals quizzes)
- Frustration Mitigation Rate (% eventos resueltos < 2 reintentos)
- Practical Transfer (ejercicios completados / presentados)

## 15. Seguridad / Riesgos
- Alucinaciones: incluir verificación factual ligera (cross-check 2ª llamada / citas)
- Contenido desactualizado: TTL en lecciones con fecha revisión.
- Sesgo: dataset de analogías auditado (diversidad cultural / género neutral).

## 16. Roadmap (MVP -> Fase 2)
| Sprint | Entregables |
|--------|-------------|
| S1 | Diagnóstico + Modelado competencias + Esqueleto agente tutor |
| S2 | Motor micro-lecciones + Reformulaciones |
| S3 | Ejercicios + Evaluador + Feedback estructurado |
| S4 | Detección frustración textual + Dashboard progreso |
| S5 | Ingesta novedades básica + Deep Dive semanal |
| Fase 2 | Voz, video, emoción multimodal, comunidad, recomendador social |

## 17. Backlog Priorizado (MoSCoW)
- Must: RF-01..RF-07, detección frustración básica, vector store lecciones
- Should: Ingesta automática, dashboard avanzado, spaced repetition planner
- Could: Voz TTS/STT, analogías personalizadas por perfil
- Won't (MVP): Expresiones faciales en tiempo real, VR, certificaciones formales

## 18. Integraciones IA Sugeridas
| Función | Herramienta / Modelo |
|---------|----------------------|
| LLM principal | GPT-4o (razonamiento + instrucciones) |
| Reformulación controlada | GPT-4o con system templates |
| Embeddings | text-embedding-3-small / Instructor-xl |
| Sentiment / Frustración | Modelo ligero open-source + heurísticas |
| Resumen ingestión | GPT-4o + filtros regex/NER |
| Evaluación código | LLM + pruebas unitarias generadas |

## 19. Formatos de Prompting (Ejemplos)
- SYSTEM: "Eres un tutor de IA. Responde en bloques estructurados: Objetivo, Explicación Breve, Ejemplo Código, Quiz (1 pregunta)."
- REFORMULATE: "Reexplica el concepto con una analogía cotidiana y luego un paso a paso numerado."
- FEEDBACK: JSON rubric {correctness, clarity, efficiency, next_action}

## 20. Métrica de Éxito Inicial (Hackathon)
- ≥ 30 micro-lecciones generadas y navegables
- ≥ 10 ejercicios evaluables
- Tasa de reformulación < 35% después de iteración 2
- Sesión promedio > 5 min

## 21. Riesgos Técnicos & Mitigaciones
| Riesgo | Impacto | Mitigación |
|--------|---------|-----------|
| Latencia LLM alta | Mala UX | Caching plantillas / streaming |
| Fuga de contexto | Respuestas irrelevantes | Ventanas contextuales dinámicas + resúmenes |
| Ingesta ruido | Degrada calidad | Filtro calidad (longitud mínima, score relevancia) |
| Sobrepersonalización | Estanca retos | Regla: 20% contenido exploratorio |

## 22. KPIs Operativos
- Latencia media respuesta
- Reformulation Rate
- Frustration Events por sesión
- Lesson Completion Rate
- Exercise Success Rate
- Weekly Active Learners

## 23. Interfaces Iniciales (Contratos JSON Simplificados)
lesson_plan {
  objectives: string[],
  prerequisites: string[],
  steps: [{title, content, codeExample?}],
  quiz: {question, options[], answer_index}
}
exercise_submission {
  user_id, exercise_id, code, timestamp
}
feedback_response {
  scores: {correctness:0-1, clarity:0-1, efficiency:0-1},
  summary, next_actions[]
}
emotion_signal {
  user_id, sentiment: "neutral"|"frustrated"|"confused", confidence:0-1
}

## 24. Conclusión
El diseño prioriza impacto pedagógico rápido, adaptabilidad cognitiva y mantenibilidad modular. El enfoque Hybrid + micro-learning + evaluación inmediata crea un loop de aprendizaje-aplicación eficiente que maximiza retención y transferencia práctica.
