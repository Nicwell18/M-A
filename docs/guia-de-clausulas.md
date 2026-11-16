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

## 3. Cláusulas pendientes

Se desarrollarán una a una, con el mismo esquema.

| Cláusula | Idea en una frase |
|---|---|
| No-shop y fiduciary out | Prohíbe buscar otras ofertas, pero deja al consejo aceptar una claramente superior |
| Material Adverse Effect | Define qué deterioro del negocio permite al comprador no cerrar |
| Efforts regulatorios | Cuánto debe sacrificar el comprador para lograr las autorizaciones |
| Outside date | La fecha límite tras la cual cualquiera puede abandonar |
| Specific performance | Si un juez puede obligar a cerrar, en vez de solo indemnizar |

---

## 4. Glosario

| Término | Significado |
|---|---|
| Break-up fee | Otro nombre de la termination fee |
| Change of recommendation | El consejo retira su recomendación de votar a favor del deal |
| Closing | Ejecución efectiva de la operación |
| End Date / Outside date | Fecha límite para cerrar |
| Enterprise value | Equity value más deuda neta |
| Equity value | Valor de las acciones de la empresa |
| Fiduciary out | Salida que permite al consejo cumplir su deber hacia los accionistas |
| Merger Sub | Filial instrumental del comprador |
| No-vote | Los accionistas votan en contra del deal |
| Signing | Firma del contrato |
| Superior proposal | Oferta de un tercero que el consejo considera mejor |
| Tail | Periodo tras la terminación en el que una operación alternativa obliga a pagar la fee |
| Willful Breach | Incumplimiento deliberado, a sabiendas |
