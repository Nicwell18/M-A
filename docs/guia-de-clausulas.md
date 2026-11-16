# Guía de cláusulas de un merger agreement

Apuntes para entender qué hace cada cláusula, por qué importa y cómo se
califica en este proyecto. Los ejemplos salen del contrato de prueba: la fusión
Trump Media (TMTG) / TAE Technologies, firmada el 18 de diciembre de 2025.

Las páginas citadas son las del PDF, no las impresas en el contrato.

---

## 1. Cómo leer un merger agreement

### Firma y cierre no ocurren el mismo día

- **Signing (firma):** las partes firman el contrato y lo anuncian.
- **Closing (cierre):** la operación se ejecuta de verdad. Llega meses después,
  porque antes hacen falta el voto de los accionistas y las autorizaciones
  regulatorias.

Casi todo el contrato existe para repartir los riesgos de ese periodo
intermedio: que aparezca otro comprador, que el negocio se deteriore, que un
regulador lo bloquee, que alguien se arrepienta.

### Las cuatro preguntas

| Pregunta | Cláusulas | ¿Se califica? |
|---|---|---|
| 1. ¿Qué recibe cada parte? | Merger consideration | No: se describe |
| 2. ¿Puede aparecer otro comprador? | No-shop, fiduciary out, termination fee | Sí |
| 3. ¿Se va a cerrar de verdad? | Conditions, MAE, efforts regulatorios, outside date | Sí |
| 4. ¿Qué pasa si se rompe? | Termination fee, specific performance | Sí |

### Quién es quién

- **Parent:** el comprador (aquí, TMTG).
- **Company** o **Target:** la empresa adquirida (aquí, TAE).
- **Merger Sub:** una filial vacía del comprador, creada solo para fusionarse
  con la Company. Es un mecanismo técnico, no una parte con intereses propios.

### El mapa de un merger agreement

| Artículo típico | Contenido | En el contrato de prueba |
|---|---|---|
| Definitions | Términos definidos; muchas cláusulas dependen de ellos | Art. I |
| The Merger / Consideration | Mecánica y precio | Arts. II y III |
| Representations and Warranties | Lo que cada parte declara que es cierto | Arts. IV y V |
| Covenants | Lo que cada parte se compromete a hacer hasta el cierre | Art. VI |
| Conditions | Lo que debe cumplirse para que haya obligación de cerrar | Art. VII |
| Termination | Cuándo se puede romper y qué cuesta | Art. VIII |
| Miscellaneous | Ley aplicable, remedios, notificaciones | Art. IX |

---

## 2. Termination fee

### Qué es

Una cantidad fija que una parte paga a la otra si el contrato se termina por
causas atribuibles a ella. También se llama **break-up fee**.

### Por qué existe

El comprador invierte meses y dinero en el deal, y al anunciarlo revela cuánto
está dispuesto a pagar. Si después llega un tercero con una oferta algo mejor y
la Company se va con él, el primer comprador ha hecho el trabajo gratis para su
competidor. La fee le compensa.

Al mismo tiempo, el consejo de la Company tiene el deber de conseguir el mejor
resultado para sus accionistas, así que no puede renunciar del todo a aceptar
una oferta superior. La fee es el precio de esa salida.

### Por qué importa su tamaño

- **Demasiado alta:** cualquier oferta rival tiene que superar el precio *más*
  la fee. Si es muy alta, nadie puja y los accionistas pierden una posible
  oferta mejor. Los tribunales de Delaware pueden considerarla una medida que
  impide ofertas rivales.
- **Demasiado baja:** el comprador queda poco protegido y el deal es fácil de
  romper.

Por eso se mide siempre como **porcentaje**, no en dólares.

### Sobre qué se mide el porcentaje

- **Equity value:** el valor de las acciones (precio por acción × número de
  acciones). Es la referencia más habitual.
- **Enterprise value:** equity value más deuda neta. Importa cuando la empresa
  está muy endeudada, porque la misma fee parece más pequeña sobre el
  enterprise value.

En este proyecto se usa el equity value **de la parte que paga**.

### Cuándo se paga: los tres supuestos típicos

| Supuesto | Qué ocurre |
|---|---|
| **Superior proposal** | Una parte termina el contrato para firmar una oferta mejor con un tercero. Paga la fee al terminar. |
| **Change of recommendation** | El consejo deja de recomendar el deal a sus accionistas y la otra parte termina el contrato. |
| **Tail** | El contrato se termina (por fecha límite, voto negativo o incumplimiento) habiendo una oferta rival pública. Si en los meses siguientes esa parte cierra una operación alternativa, paga la fee entonces. |

El **tail** existe para evitar una trampa: dejar morir el deal, no pagar nada, y
firmar con el rival al día siguiente.

### Términos que la acompañan

- **Reverse termination fee:** la fee que paga el *comprador*, normalmente si
  falla la financiación o la autorización regulatoria. Suele ser más alta.
- **Expense reimbursement:** reembolso de gastos, con un tope, cuando los
  accionistas votan en contra sin que haya una oferta rival.
- **Sole and exclusive remedy:** cobrada la fee, no se puede reclamar nada más.
  Suele exceptuarse el incumplimiento deliberado (**Willful Breach**) y el
  fraude.

### Qué dice el contrato de prueba

| Término | Contenido | Dónde |
|---|---|---|
| Importe | 90 millones de dólares, igual para ambas partes | Section 1.1, "Company Termination Fee" y "Parent Termination Fee" |
| Supuestos | Superior proposal, change of recommendation y tail, para cada parte | Section 8.3(a) y 8.3(b), pp. 121-122 |
| Tail | 12 meses; la operación alternativa debe ser por más del 50% | Section 8.3(a)(i) y 8.3(b)(i) |
| Gastos | Hasta 30 millones si los accionistas votan en contra | Section 8.3(c) y Section 1.1, "Company Expenses" |
| Remedio exclusivo | Sí, salvo Willful Breach o Fraud | Section 8.3(e), p. 123 |

Cita de la cuantía: *"Company Termination Fee" means an amount equal to
$90,000,000.*

Es una fee **simétrica** porque el deal es una fusión en acciones entre dos
partes de tamaño parecido: las dos necesitan el voto de sus accionistas y las
dos podrían recibir una oferta rival.

### Estándar de mercado y veredicto

| Fee sobre el equity value de quien paga | Veredicto |
|---|---|
| Menos del 2,0% | off-market (favorece a quien paga) |
| 2,0% – 3,5% | market |
| 3,5% – 4,0% | off-market |
| Más del 4,0% | aggressive |

Fuentes: DealLawyers.com (mayo de 2025), rango habitual del 2,0% al 3,5% del
equity value; Houlihan Lokey, estudio de 2024, mediana del 2,5%–2,6% del valor
de la transacción. El umbral del 4,0% es criterio propio.

**En el contrato de prueba:** 90 millones sobre unos 3.000 millones por parte
es aproximadamente un 3,0%, es decir, **market**. El reparto 50/50 del valor
anunciado (más de 6.000 millones) es una hipótesis sin verificar.

### Preguntas de entrevista

- **¿Por qué una termination fee no puede ser del 10%?** Porque impediría de
  hecho cualquier oferta rival, y el consejo incumpliría su deber hacia los
  accionistas.
- **¿Equity value o enterprise value?** Equity value es la referencia habitual;
  en empresas muy endeudadas conviene mirar los dos.
- **¿Qué es el tail y para qué sirve?** Ver arriba: evita que una parte deje
  caer el deal para firmar con el rival sin pagar.
- **¿Qué diferencia hay entre termination fee y reverse termination fee?** Quién
  paga y por qué: la primera, la Company por irse con otro; la segunda, el
  comprador por no poder cerrar.

---

## 3. No-shop y fiduciary out

### Qué es

- **No-shop (no solicitation):** desde la firma, la parte se compromete a no
  buscar ofertas alternativas ni negociar con terceros.
- **Fiduciary out:** la excepción. Si llega una oferta no solicitada que es
  claramente mejor, el consejo puede atenderla, porque su deber hacia los
  accionistas no se puede eliminar por contrato.

### Por qué existe

Es la otra mitad de la termination fee. El comprador quiere que su deal no se
use como suelo para una subasta; el consejo necesita poder aceptar algo mejor.
El resultado típico: no se puede *buscar*, pero sí *responder*.

### Las piezas

| Pieza | Qué regula |
|---|---|
| **Alternative / Acquisition Proposal** | Qué cuenta como oferta rival. Suele bastar con el 15%-20% de las acciones o activos |
| **Window-shop** | Permiso para dar información y negociar con quien presente una oferta no solicitada que pueda llevar a una superior |
| **Superior Proposal** | Oferta por la mayoría de la empresa (normalmente más del 50%) que el consejo considera mejor |
| **Match right** | Antes de aceptar la oferta superior, hay que avisar a la contraparte y darle unos días para igualarla |
| **Fiduciary termination right** | Derecho a terminar el contrato para firmar la oferta superior, pagando la fee |
| **Change of recommendation** | El consejo retira su recomendación; puede deberse a una oferta superior o a un **intervening event** (un hecho nuevo e imprevisible) |
| **Go-shop** | Lo contrario del no-shop: un periodo inicial en el que sí se pueden buscar ofertas. Poco habitual entre compradores estratégicos |

### Qué lo hace agresivo

- Que el consejo no pueda terminar el contrato y solo pueda cambiar su
  recomendación (**force the vote**): el deal se vota igualmente.
- Que no haya salida fiduciaria de ningún tipo.
- Un match right muy largo, que da ventaja a la contraparte y desanima al
  tercero.

### Qué dice el contrato de prueba

Es simétrico: la Section 6.5 obliga a la Company y la 6.6 a Parent, con los
mismos términos.

| Término | Contenido | Dónde |
|---|---|---|
| Umbral de oferta rival | Más del 20% de activos o acciones | Section 1.1, "Company Alternative Proposal" |
| Superior Proposal | El mismo concepto con el umbral elevado al 50% | Section 1.1, "Company Superior Proposal" |
| Window-shop | Permitido hasta el voto de los accionistas, con acuerdo de confidencialidad | Section 6.5(b) |
| Aviso de ofertas | En 24 horas | Section 6.5(c) |
| Fiduciary out | Puede cambiar la recomendación y terminar el contrato para firmar la oferta superior | Section 6.5(d) y 8.1(c)(iii) |
| Intervening event | Permite cambiar la recomendación, no terminar | Section 6.5(d) |
| Match right | 5 días hábiles; 4 más por cada mejora de la oferta, sin límite de rondas | Section 6.5(d)(i)-(iii) |

Un detalle de redacción: la Section 6.5(f) dice que el incumplimiento de los
representantes de la Company se considera incumplimiento "by Parent". Por el
contexto parece una errata por "by Company". Es el tipo de cosa que un
abogado revisa y que una herramienta automática no debe corregir por su cuenta.

### Estándar y veredicto

| Dato | Market | Off-market | Aggressive |
|---|---|---|---|
| Fiduciary out | Puede terminar por oferta superior | Solo cambio de recomendación | Ninguna salida |
| Match right inicial | Hasta 5 días hábiles | 6 a 10 | Más de 10 |

Son criterios propios, pendientes de contrastar con el ABA Deal Points Study.

**En el contrato de prueba:** ambos datos son **market** para las dos partes.

### Preguntas de entrevista

- **¿Qué diferencia hay entre no-shop y go-shop?** El no-shop prohíbe buscar
  ofertas; el go-shop lo permite durante un periodo inicial.
- **¿Por qué no se puede pactar un no-shop sin excepciones?** Porque el consejo
  no puede renunciar por contrato a su deber fiduciario.
- **¿Para qué sirve el match right?** Da al primer comprador la última palabra y
  encarece el intento de un tercero.

---

## 4. Material Adverse Effect (MAE)

### Qué es

La definición del deterioro del negocio que permite a la otra parte negarse a
cerrar. También se llama **MAC** (Material Adverse Change).

### Cómo funciona

No suele ser una cláusula propia, sino una definición que se usa en dos sitios:

- como **condición de cierre**: "que no haya ocurrido un MAE desde la firma";
- como **calificador** de las representations: una declaración falsa solo
  importa si la falsedad supone un MAE.

### La estructura de la definición

1. **Regla general:** cualquier efecto materialmente adverso sobre el negocio.
2. **Carve-outs (exclusiones):** riesgos que no cuentan aunque dañen el negocio:
   economía general, cambios en el sector, cambios legales o contables, guerra,
   catástrofes, pandemias, el propio anuncio del deal, no cumplir previsiones.
3. **Disproportionate effect:** algunas exclusiones dejan de aplicarse si el
   daño afecta a la empresa de forma desproporcionada frente a su sector.

La lógica: el comprador asume los riesgos generales del mercado; el vendedor,
los riesgos específicos de su empresa.

### Por qué importa

- **Pocas exclusiones** favorecen al comprador: más situaciones le permiten
  no cerrar.
- **Muchas exclusiones sin la salvedad** favorecen al vendedor: casi nada le
  permite al comprador salir.

En la práctica, un tribunal casi nunca aprecia un MAE. El caso de referencia
es *Akorn v. Fresenius* (Delaware, 2018), la primera vez que se aceptó. Por eso
la cláusula funciona sobre todo como palanca para renegociar el precio.

### Qué dice el contrato de prueba

| Término | Contenido | Dónde |
|---|---|---|
| Exclusiones (Company) | Diez, de la (i) a la (x): economía y mercados, sector, anuncio del deal, cumplimiento del contrato, guerra, catástrofes, cambios legales, GAAP, previsiones, pandemias | Section 1.1, "Company Material Adverse Effect" |
| Disproportionate effect | Se aplica a siete de las diez exclusiones | La misma definición, inciso final |
| Parent | Definición equivalente, con doce exclusiones | Section 1.1, "Parent Material Adverse Effect" |

Las exclusiones mencionan expresamente los mercados de **Digital Assets**: un
ejemplo de cómo la definición se adapta al negocio de las partes.

### Estándar y veredicto

| Exclusiones | Veredicto |
|---|---|
| Amplias, con disproportionate effect | market |
| Amplias, sin disproportionate effect | off-market |
| Pocas o ninguna | aggressive |

Criterio propio. No se analiza cada exclusión por separado.

**En el contrato de prueba:** **market** para las dos partes.

### Preguntas de entrevista

- **¿Qué es un carve-out?** Un riesgo excluido de la definición de MAE.
- **¿Para qué sirve el disproportionate effect?** Devuelve al vendedor el
  riesgo cuando un problema general le golpea más que a sus competidores.
- **¿Es fácil invocar un MAE?** No. Los tribunales exigen un deterioro
  sustancial y duradero; se usa más para renegociar que para romper.

---

## 5. Efforts regulatorios

### Qué es

El compromiso de las partes de hacer lo necesario para obtener las
autorizaciones regulatorias: competencia (en EE. UU., la **HSR Act**),
inversión extranjera y reguladores sectoriales.

### Las dos preguntas

**1. ¿Con qué nivel de esfuerzo?**

| Estándar | Exigencia |
|---|---|
| Best efforts | La más alta; poco usada |
| Reasonable best efforts | La habitual |
| Commercially reasonable efforts | Más débil |

**2. ¿Hay que aceptar remedios?** Si el regulador exige vender un negocio o
aceptar restricciones para aprobar el deal:

| Compromiso | Qué significa |
|---|---|
| **Hell or high water** | Hay que aceptar cualquier remedio, sin límite |
| Limitado | Hay que aceptar remedios hasta un tope pactado |
| Sin regular | Solo rige el estándar general de esfuerzo |
| Excluido expresamente | Nadie está obligado a aceptar ningún remedio |

### Por qué importa

Decide quién soporta el riesgo regulatorio. Con *hell or high water*, el
comprador; con la exclusión expresa, el deal puede caerse si el regulador pide
algo. Suele ir ligada a una reverse termination fee: quien no acepta remedios,
paga si el deal no se aprueba.

Su peso real depende de cuánto se solapen los negocios de las partes. Si no
compiten entre sí, el riesgo de competencia es bajo y la cláusula importa poco.

### Qué dice el contrato de prueba

| Término | Contenido | Dónde |
|---|---|---|
| Estándar | Reasonable best efforts, para todas las partes | Section 6.10(a) |
| Plazo HSR | Notificación en 20 días hábiles | Section 6.10(b) |
| Litigar | Obligación de defender el deal hasta resolución firme | Section 6.10(c) |
| Remedios | Ninguna parte está obligada a aceptar desinversiones ni restricciones | Section 6.10(d) |
| No empeorar | Prohibido hacer adquisiciones que retrasen las autorizaciones | Section 6.10(e) |

### Estándar y veredicto

| Dato | Market | Off-market |
|---|---|---|
| Estándar de esfuerzo | Reasonable best efforts | Best efforts; commercially reasonable efforts |
| Remedios | Limitado; sin regular | Hell or high water; excluido expresamente |

Criterio propio.

**En el contrato de prueba:** estándar **market**; remedios **off-market**,
porque se excluyen expresamente. Es la única cláusula del contrato que sale de
mercado. Matiz: Trump Media y TAE operan en sectores distintos, así que el
riesgo de competencia parece bajo; el veredicto señala la redacción, no un
problema probable.

### Preguntas de entrevista

- **¿Qué es hell or high water?** La obligación de aceptar cualquier remedio que
  pida el regulador para aprobar el deal.
- **¿Qué relación tiene con la reverse termination fee?** Son alternativas para
  repartir el mismo riesgo: o el comprador se obliga a aceptar remedios, o paga
  si el deal no se aprueba.

---

## 6. Outside date

### Qué es

La fecha límite para cerrar. Si llega sin cierre, cualquiera de las partes
puede terminar el contrato. También se llama **End Date**, **Termination Date**
o **drop-dead date**.

### Por qué importa

- **Corta:** si las autorizaciones se retrasan, el deal muere o hay que
  renegociar la prórroga, y eso da poder a quien quiera salir.
- **Larga:** las partes quedan atadas durante mucho tiempo, sujetas a las
  restricciones del periodo intermedio y expuestas a que el mercado cambie.

### Elementos habituales

- **Prórrogas automáticas** si solo faltan las autorizaciones regulatorias.
- **Salvedad de incumplimiento:** no puede terminar por fecha límite quien ha
  causado el retraso.
- Relación con la fee: terminar por fecha límite con una oferta rival pendiente
  puede activar el tail.

### Qué dice el contrato de prueba

| Término | Contenido | Dónde |
|---|---|---|
| Fecha límite | 18 de diciembre de 2026: doce meses desde la firma | Section 8.1(b)(i) |
| Prórrogas | Ninguna | Section 8.1(b)(i) |
| Salvedad | No puede invocarla quien haya sido la causa principal del retraso | Section 8.1(b)(i) |

### Estándar y veredicto

| Meses desde la firma | Veredicto |
|---|---|
| Hasta 3 | off-market (muy corto) |
| 3 a 12 | market |
| 12 a 18 | off-market (largo) |
| Más de 18 | aggressive |

Criterio propio; no se tienen en cuenta las prórrogas.

**En el contrato de prueba:** 12 meses, **market**, en el límite del tramo.

### Preguntas de entrevista

- **¿Qué pasa si llega la outside date sin cierre?** Cualquiera puede terminar
  el contrato, salvo quien haya causado el retraso.
- **¿Por qué se pactan prórrogas automáticas?** Para no perder un deal al que
  solo le falta una autorización que está en trámite.

---

## 7. Specific performance

### Qué es

El derecho a pedir a un juez que obligue a la otra parte a cumplir el contrato
(incluido cerrar la operación), en lugar de limitarse a reclamar una
indemnización.

### Por qué importa

Sin cumplimiento forzoso, quien se arrepiente solo arriesga daños o una fee:
el contrato funciona como una opción. Con él, el contrato obliga de verdad.
Los daños son además difíciles de probar en un deal fallido, y por eso las
partes declaran que no son remedio suficiente.

### Variantes

| Variante | Dónde se ve |
|---|---|
| Plena y mutua | Deals entre compradores estratégicos |
| Condicionada a la financiación | Compradores financieros (private equity): solo se puede obligar a cerrar si la deuda está disponible; si no, se cobra la reverse termination fee |
| Unilateral | Poco frecuente |
| Ninguna | El único remedio es la fee |

### Qué dice el contrato de prueba

| Término | Contenido | Dónde |
|---|---|---|
| Disponibilidad | Cualquier parte puede exigir el cumplimiento, incluido el cierre | Section 9.5(a) |
| Compatibilidad | No lo impide que exista un remedio monetario | Section 9.5(a) |
| Sin oposición ni fianza | Nadie alegará que los daños bastan, ni se exige fianza | Section 9.5(b) |

Encaja con la Section 8.3(e): la fee es remedio exclusivo *después* de
terminar el contrato; antes de terminarlo, se puede exigir el cumplimiento.

### Estándar y veredicto

| Disponibilidad | Veredicto |
|---|---|
| Plena y mutua | market |
| Condicionada a la financiación | off-market |
| Unilateral | off-market |
| Ninguna | aggressive |

Criterio propio.

**En el contrato de prueba:** **market**.

### Preguntas de entrevista

- **¿Por qué no bastan los daños?** Porque son difíciles de cuantificar y no
  devuelven la operación a quien quería cerrarla.
- **¿Qué cambia con un comprador de private equity?** El cumplimiento forzoso
  suele estar condicionado a que la financiación esté disponible.

---

## 8. Resumen del contrato de prueba

| Cláusula | Dato | Veredicto |
|---|---|---|
| Termination fee | 90 millones por parte, en torno al 3,0% | market |
| Fiduciary out | Terminación por oferta superior | market |
| Match right | 5 días hábiles | market |
| MAE | Exclusiones amplias con disproportionate effect | market |
| Estándar de esfuerzo | Reasonable best efforts | market |
| Remedios regulatorios | Excluidos expresamente | off-market |
| Outside date | 12 meses | market |
| Specific performance | Plena y mutua | market |

Estos datos proceden de una lectura manual del contrato
(`data/reference/tmtg_tae_manual_findings.yaml`), con las citas verificadas
por el programa. La tabla completa con citas está en `docs/ejemplo-informe.md`.

---

## 9. Glosario

| Término | Significado |
|---|---|
| Break-up fee | Otro nombre de la termination fee |
| Carve-out | Riesgo excluido de la definición de MAE |
| Change of recommendation | El consejo retira su recomendación de votar a favor del deal |
| Closing | Ejecución efectiva de la operación |
| Disproportionate effect | Salvedad que devuelve al vendedor un riesgo general si le afecta más que a su sector |
| End Date / Outside date | Fecha límite para cerrar |
| Enterprise value | Equity value más deuda neta |
| Equity value | Valor de las acciones de la empresa |
| Fiduciary out | Salida que permite al consejo cumplir su deber hacia los accionistas |
| Force the vote | Obligación de someter el deal a votación aunque el consejo cambie su recomendación |
| Go-shop | Periodo inicial en el que sí se pueden buscar ofertas alternativas |
| Hell or high water | Obligación de aceptar cualquier remedio regulatorio, sin límite |
| HSR Act | Ley estadounidense de notificación previa de concentraciones |
| Intervening event | Hecho nuevo e imprevisible que permite al consejo cambiar su recomendación |
| MAE / MAC | Material Adverse Effect / Change: deterioro que permite no cerrar |
| Match right | Derecho a igualar una oferta rival antes de que se acepte |
| Merger Sub | Filial instrumental del comprador |
| No-shop | Prohibición de buscar o negociar ofertas alternativas |
| No-vote | Los accionistas votan en contra del deal |
| Reverse termination fee | Fee que paga el comprador si no puede cerrar |
| Signing | Firma del contrato |
| Specific performance | Cumplimiento forzoso del contrato ordenado por un juez |
| Superior proposal | Oferta de un tercero que el consejo considera mejor |
| Tail | Periodo tras la terminación en el que una operación alternativa obliga a pagar la fee |
| Willful Breach | Incumplimiento deliberado, a sabiendas |
| Window-shop | Permiso para atender ofertas no solicitadas |
