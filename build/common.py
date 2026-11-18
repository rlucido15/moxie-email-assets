# Spanish strings shared by several pages (disclosures, form consent, buttons, review chrome).
# Customer reviews are left in the reviewer's own words (English) on purpose.
T = {
    "Get pre-approved": "Obtén tu preaprobación",
    "Get pre-approved today": "Obtén tu preaprobación hoy",
    "Get approved now": "Obtén tu aprobación",
    "Get expert guidance": "Habla con un experto",
    "Read more →": "Leer más →",
    "Read more": "Leer más",
    "Show less": "Ver menos",
    "Google": "Google",
    "5 out of 5 stars": "5 de 5 estrellas",
    "Rated 5 out of 5 stars on Google": "Calificación de 5 de 5 estrellas en Google",
    "Read all reviews on Google →": "Lee todas las reseñas en Google →",
    "Scotsman Guide Top Originators badge": "Insignia de Top Originators de Scotsman Guide",
    "Scotsman Guide": "Scotsman Guide",
    "Top Originator": "Top Originator",
    "Google user": "Usuario de Google",
    "Moxie": "Moxie",
    "Previous": "Anterior",
    "Next": "Siguiente",
    "Previous reviews": "Reseñas anteriores",
    "More reviews": "Más reseñas",
    "Close": "Cerrar",
    "Menu": "Menú",
    "Loan amount": "Monto del préstamo",
    "a month": "al mes",
    "per month": "al mes",
    "/mo": "/mes",
    "Disclosures": "Divulgaciones",
    "Name *": "Nombre *",
    "Phone *": "Teléfono *",
    "Email *": "Correo electrónico *",
    "Message": "Mensaje",
    "Website": "Sitio web",
    "Submit application": "Enviar solicitud",
    "Sending…": "Enviando…",
    "Select states": "Selecciona estados",
    "Please fill in all required fields.": "Completa todos los campos obligatorios.",
    "Please enter a 10-digit phone number.": "Ingresa un número de teléfono de 10 dígitos.",
    "Please enter a valid email address.": "Ingresa un correo electrónico válido.",
    "Please check the consent box to continue.": "Marca la casilla de consentimiento para continuar.",
    "Application received.": "Solicitud recibida.",
    # TCPA consent (shared by the application forms) - have a bilingual reviewer confirm
    "I agree to the": "Acepto el",
    "Electronic Disclosure Consent Agreement": "Acuerdo de consentimiento para divulgaciones electrónicas",
    "and to receive recurring marketing communications from Moxie Mortgage, including auto-dialed calls, texts, and prerecorded or artificial voice messages. Frequency varies; message and data rates may apply. Reply STOP to opt out or HELP for help. I agree to the":
        "y a recibir comunicaciones de marketing recurrentes de Moxie Mortgage, incluidas llamadas con marcación automática, mensajes de texto y mensajes de voz pregrabados o artificiales. La frecuencia varía; pueden aplicarse tarifas de mensajes y datos. Responde STOP para cancelar o HELP para obtener ayuda. Acepto los",
    "Terms of Service": "Términos del servicio",
    "and": "y",
    "Privacy Policy": "Política de privacidad",
    ". Consent is not required to make a purchase; call 480.660.2518 for direct assistance.":
        ". El consentimiento no es un requisito para realizar una compra; llama al 480.660.2518 para recibir ayuda directa.",
    "Moxie Mortgage · NMLS #1660690 · AZMB 0944059 · Equal Housing Lender": "Moxie Mortgage · NMLS #1660690 · AZMB 0944059 · Prestamista con igualdad de oportunidades de vivienda",
    "Equal Housing Lender": "Prestamista con igualdad de oportunidades de vivienda",
    "Equal Housing Opportunity": "Igualdad de oportunidades de vivienda",
    "Not a commitment to lend; all loans are subject to credit approval.": "No es un compromiso de préstamo; todos los préstamos están sujetos a la aprobación de crédito.",
    "Serving 51 states and territories": "Al servicio de 51 estados y territorios",
}
R = [
    [r"^(\d+) out of 5 stars$", r"$1 de 5 estrellas"],
    [r"^Year (\d+)$", r"Año $1"],
    [r"^Call (\d{3}\.\d{3}\.\d{4})$", r"Llama al $1"],
    [r"^Call (\(\d{3}\) \d{3}-\d{4})$", r"Llama al $1"],
]
# Fallback reviews shown before the review library loads (buy, home, about). The library itself carries text_es.
T.update({
    "“They held our hand every step of the way, explaining every detail with patience and clarity. Thank you, Moxie Mortgage, for making our dream of homeownership a reality!”":
        "“Nos llevaron de la mano en cada paso, explicándonos cada detalle con paciencia y claridad. ¡Gracias, Moxie Mortgage, por hacer realidad nuestro sueño de tener casa propia!”",
    "“Calvin made what is usually a stressful process completely seamless. His professionalism, transparency, and attention to detail gave me complete confidence that I was in the best hands.”":
        "“Calvin convirtió lo que normalmente es un proceso estresante en algo completamente sencillo. Su profesionalismo, transparencia y atención al detalle me dieron total confianza de que estaba en las mejores manos.”",
    "“Alex Salomons of Moxie Mortgage was great to work with. She was very patient and helpful, guided us through the entire process, provided options, and answered all our questions.”":
        "“Fue genial trabajar con Alex Salomons de Moxie Mortgage. Fue muy paciente y servicial, nos guio en todo el proceso, nos dio opciones y respondió todas nuestras preguntas.”",
    "“Robert and his team provided a speedy and FLAWLESS execution in our loan process. We cannot be more grateful for being referred to Robert and look forward to working with the Moxie team again in the future! Mahalo!”":
        "“Robert y su equipo hicieron una ejecución rápida e IMPECABLE de nuestro proceso de préstamo. ¡No podríamos estar más agradecidos de que nos refirieran con Robert y esperamos volver a trabajar con el equipo de Moxie en el futuro! ¡Mahalo!”",
    "“Working with Calvin and the team at Moxie Mortgage was an absolute pleasure from start to finish. Calvin made what is usually a stressful process completely seamless.”":
        "“Trabajar con Calvin y el equipo de Moxie Mortgage fue un verdadero placer de principio a fin. Calvin convirtió lo que normalmente es un proceso estresante en algo completamente sencillo.”",
    "“We recently closed on a HELOC with Moxie Mortgage and could not have been happier with the entire experience!! Our loan officer, Alex, went above and beyond to ensure a smooth and seamless process from start to finish.”":
        "“¡¡Hace poco cerramos una línea de crédito sobre el valor de nuestra casa (HELOC) con Moxie Mortgage y no podríamos estar más contentos con toda la experiencia!! Nuestra oficial de préstamos, Alex, hizo más de lo esperado para asegurar un proceso fácil y sin contratiempos de principio a fin.”",
    "“Robert and team did amazing! As a first-time homebuyer, each step of the way I was met with knowledge, quick responses, questions answered and an accurate timeline to make sure I would close in a timely manner.”":
        "“¡Robert y su equipo hicieron un trabajo increíble! Como comprador de vivienda por primera vez, en cada paso recibí conocimiento, respuestas rápidas, respuestas a mis preguntas y un calendario preciso para asegurar que cerrara a tiempo.”",
    "“Robert at Moxie Mortgage was incredible! He went above and beyond, pulling out all the stops to make sure our deal got done. He was responsive, solution-oriented, and truly fought for us every step of the way.”":
        "“¡Robert de Moxie Mortgage fue increíble! Hizo más de lo esperado y no escatimó esfuerzos para asegurar que nuestro trato se cerrara. Respondió rápido, se enfocó en soluciones y realmente luchó por nosotros en cada paso.”",
    "5 out of 5 stars": "5 de 5 estrellas",
})
