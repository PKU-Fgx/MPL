# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  #
#                               1. NER
# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  #
TEMPLATE_NER_nl = """
Given Label Set:
{entities_defination}

Given Sentence:
"{input_text}"

Extracted Entities:
<SPLIT>
{output_text}
End.
""".strip()

TEMPLATE_NER_python = """
def named_entity_recognition(input_text: str):
    \"""
    Task: Named entity recognition (NER) involves identifying and classifying named entities in text into predefined categories.
    
    Label Set:
{entities_defination}

    Example:
        >>> entity_list = named_entity_recognition('I love traveling in America.')
        >>> entity_list.append(gpe_gpe('America'))  # Means 'America' is a `geographic` entity
        >>> entity_list.append(per_per('I'))  # Means 'I' is a `person` entity
    \"""
    return entity_list

input_text = "{input_text}"
entity_list = named_entity_recognition(input_text)
<SPLIT>
{output_text}
# End
""".strip()

TEMPLATE_NER_cpp = """
vector<Entity*> named_entity_recognition(const string& inputText) {{
    /*
    Task: Named entity recognition (NER) involves identifying and classifying named entities in text into predefined categories.
    
    Label Set:
{entities_defination}

    Example:
        vector<Entity*> entityList = named_entity_recognition('I love traveling in America.');
        entityList.push_back(new gpe_gpe("America"));  // Means 'America' is a `geographic` entity
        entityList.push_back(new per_per("I"));  // Means 'I' is a `person` entity
    */
    return entityList;
}}

int main() {{
    string inputText = "{input_text}";
    vector<Entity*> entityList = named_entity_recognition(inputText);
<SPLIT>
{output_text}
    return 0;
}}
""".strip()

TEMPLATE_NER_java = """
public class Main {{
    public static List<Entity> named_entity_recognition(String inputText) {{
        /**
    Task: Named entity recognition (NER) involves identifying and classifying named entities in text into predefined categories.
    
    Label Set:
{entities_defination}

    Example:
        List<Entity> entityList = named_entity_recognition('I love traveling in America.');
        entityList.add(new gpe_gpe("America"));  // Means 'America' is a `geographic` entity
        entityList.add(new per_per("I"));  // Means 'I' is a `person` entity
         */
        return entityList;
    }}

    public static void main(String[] args) {{
        String inputText = "{input_text}";
        List<Entity> entityList = named_entity_recognition(inputText);
<SPLIT>
{output_text}
    }}
}}
""".strip()

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  #
#                               2. RE
# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  #
TEMPLATE_RE_nl = """
Given Label Set:
{relations_defination}

Given Sentence:
"{input_text}"

Given Entities in the Sentence:
"{entities}"

Extracted Relations with their entities:
<SPLIT>
{output_text}
End.
""".strip()

TEMPLATE_RE_python = """
def relation_extraction(input_text: str):
    \"""
    Task Definition: Relation extraction aims to identify pairs of related entities in the given text and classify the type of relationship between them.
    
    Label Set:
{relations_defination}

    Example:
        >>> relation_list = relation_extraction('The application form requests a copy of your most recent pay stub for verification purposes.')
        >>> relation_list.append(content_container_content_container("application form", "pay stub"))  # Means that the 'application form' contains the 'pay stub'
    \"""
    return relation_list

input_text = "{input_text}"
entities_in_input_text = [{entities}]
relation_list = relation_extraction(input_text)
<SPLIT>
{output_text}
# End
""".strip()

TEMPLATE_RE_cpp = """
vector<Relation*> relation_extraction(const string& inputText) {{
    /*
    Task Definition: Relation extraction aims to identify pairs of related entities in the given text and classify the type of relationship between them.
    
    Label Set:
{relations_defination}

    Example:
        vector<Relation*> relationList = relation_extraction('The application form requests a copy of your most recent pay stub for verification purposes.');
        relationList.push_back(new content_container_content_container("application form", "pay stub"));  // Means that the 'application form' contains the 'pay stub'
    */
    return relationList;
}}

int main() {{
    string inputText = "{input_text}";  // Entities in input text: [{entities}]
    vector<Relation*> relationList = relation_extraction(inputText);
<SPLIT>
{output_text}
    return 0;
}}
""".strip()

TEMPLATE_RE_java = """
public class Main {{
    public static List<Relation> relation_extraction(String inputText) {{
        /**
    Task Definition: Relation extraction aims to identify pairs of related entities in the given text and classify the type of relationship between them.
    
    Label Set:
{relations_defination}

    Example:
        List<Relation> relationList = relation_extraction('The application form requests a copy of your most recent pay stub for verification purposes.');
        relationList.add(new content_container_content_container("application form", "pay stub"));  // Means that the 'application form' contains the 'pay stub'
         */
        return relationList;
    }}

    public static void main(String[] args) {{
        String inputText = "{input_text}";  // Entities in input text: [{entities}]
        List<Relation> relationList = relation_extraction(inputText);
<SPLIT>
{output_text}
    }}
}}
""".strip()

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  #
#                               3. EAE
# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  #
TEMPLATE_EAE_nl = """
Given Label Set:
{arguments_defination}

Given Sentence:
"{input_text}"

Given Trigger Word in the Sentence: "{trigger}"
Given Event Type of the Trigger Word: "{event_type}"

Extracted Arguments of the given Trigger:
<SPLIT>
{output_text}
End.
""".strip()

TEMPLATE_EAE_python = """
def event_arguments_extraction(input_text: str, trigger_word: str, trigger_event_type: str):
    \"""
    Task Definition: Identify and extract argument information from the input text based on the specified trigger word and its associated event type.
    
    Label Set:
{arguments_defination}

    Example:
        >>> trigger_word = "dispute"
        >>> trigger_event_type = "conflict_diplomatic"
        >>> arguments_list = event_arguments_extraction('Due to the trade dispute, the US imposed sanctions on Iran.')
        >>> arguments_list.append(Cause("trade dispute")))  # Means 'trade dispute' is the cause.
        >>> arguments_list.append(Actor("US"))  # Means the participant is the 'US'.
        >>> arguments_list.append(Target("Iran"))  # Means the target is 'Iran'.
    \"""
    return arguments_list

input_text = "{input_text}"
trigger_word = "{trigger}"
trigger_event_type = "{event_type}"
arguments_list = event_arguments_extraction(input_text, trigger_word, trigger_event_type)
<SPLIT>
{output_text}
# End
""".strip()

TEMPLATE_EAE_cpp = """
vector<Arguments*> event_arguments_extraction(const string& inputText, const string& triggerWord, const string& triggerEventType) {{
    /*
    Task Definition: Identify and extract argument information from the input text based on the specified trigger word and its associated event type.
    
    Label Set:
{arguments_defination}

    Example:
        string triggerWord = "dispute";
        string triggerEventType = "conflict_diplomatic";
        vector<Arguments*> argumentsList = event_arguments_extraction('Due to the trade dispute, the US imposed sanctions on Iran.');
        argumentsList.push_back(new Cause("trade dispute")));  // Means 'trade dispute' is the cause.
        argumentsList.push_back(new Actor("US"));  // Means the participant is the 'US'.
        argumentsList.push_back(new Target("Iran"));  // Means the target is 'Iran'.
    */
    return argumentsList;
}}

int main() {{
    string inputText = "{input_text}";
    string triggerWord = "{trigger}";
    string triggerEventType = "{event_type}";
    vector<Arguments*> argumentsList = event_arguments_extraction(inputText, triggerWord, triggerEventType);
<SPLIT>
{output_text}
    return 0;
}}
""".strip()

TEMPLATE_EAE_java = """
public class Main {{
    public static List<Arguments> event_arguments_extraction(String inputText, String triggerWord, String triggerEventType) {{
        /**
    Task Definition: Identify and extract argument information from the input text based on the specified trigger word and its associated event type.
    
    Label Set:
{arguments_defination}

    Example:
        String triggerWord = "dispute";
        String triggerEventType = "conflict_diplomatic";
        List<Arguments> argumentsList = event_arguments_extraction('Due to the trade dispute, the US imposed sanctions on Iran.');
        argumentsList.add(new Cause("trade dispute")));  // Means 'trade dispute' is the cause.
        argumentsList.add(new Actor("US"));  // Means the participant is the 'US'.
        argumentsList.add(new Target("Iran"));  // Means the target is 'Iran'.
         */
        return argumentsList;
    }}

    public static void main(String[] args) {{
        String inputText = "{input_text}";
        String triggerWord = "{trigger}";
        String triggerEventType = "{event_type}";
        List<Arguments> argumentsList = event_arguments_extraction(inputText, triggerWord, triggerEventType);
<SPLIT>
{output_text}
    }}
}}
""".strip()

# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  #
#                               4. EE
# -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  -  #
TEMPLATE_EE_nl = """
Given Label Set:
{events_defination}

Given Sentence:
"{input_text}"

Extracted Events with its trigger and arguments:
<SPLIT>
{output_text}
End.
""".strip()

TEMPLATE_EE_python = """
def event_extraction(input_text: str):
    \""" 
    Task: Identify and extract events and their related information (such as event types, arguments and role type) from text.
    
    Label Set:
{events_defination}

    Example:
        >>> event_list = event_extraction('Before joining the company, Alex Smith worked at a leading tech firm and then moved to a startup where he met his future wife.')
        >>> event_list.append(life_work("worked", [Arguments("Alex Smith", "Person"), Arguments("leading tech firm", "Organization")]))  # Means the word 'worked' triggers the `life_work` event, where the two main arguments are 'Alex Smith' and 'leading tech firms'
    \"""
    return events_list
    
input_text = "{input_text}"
event_list = event_extraction(input_text)
<SPLIT>
{output_text}
# End
""".strip()

TEMPLATE_EE_cpp = """
vector<Event*> event_extraction(const string& inputText) {{
    /*
    Task: Identify and extract events and their related information (such as event types, arguments and role type) from text.
    
    Label Set:
{events_defination}

    Example:
        vector<Event*> eventList = event_extraction('Before joining the company, Alex Smith worked at a leading tech firm and then moved to a startup where he met his future wife.');
        eventList.push_back(new life_work("worked", {{Arguments("Alex Smith", "Person"), Arguments("leading tech firm", "Organization")}}));  // Means the word 'worked' triggers the `life_work` event, where the two main arguments are 'Alex Smith' and 'leading tech firms'
    */
    return eventList;
}}

int main() {{
    string inputText = "{input_text}";
    vector<Event*> eventList = event_extraction(inputText);
<SPLIT>
{output_text}
    return 0;
}}
""".strip()

TEMPLATE_EE_java = """
public class Main {{
    public static List<Event> event_extraction(String inputText) {{
        /**
    Task: Identify and extract events and their related information (such as event types, arguments and role type) from text.
    
    Label Set:
{events_defination}

    Example:
        List<Event> eventList = event_extraction('Before joining the company, Alex Smith worked at a leading tech firm and then moved to a startup where he met his future wife.');
        eventList.add(new life_work("worked", List.of(new Arguments("Alex Smith", "Person"), new Arguments("leading tech firm", "Organization"))));  // Means the word 'worked' triggers the `life_work` event, where the two main arguments are 'Alex Smith' and 'leading tech firms'
         */
        return eventList;
    }}

    public static void main(String[] args) {{
        String inputText = "{input_text}";
        List<Event> eventList = event_extraction(inputText);
<SPLIT>
{output_text}
    }}
}}
""".strip()