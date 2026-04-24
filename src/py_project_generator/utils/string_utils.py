import re
class StringUtils:
    @staticmethod
    def sluggify(text):
        """Convert string to hyphen-separated format"""
        if not text:
            return ""
        # Convert to lowercase first
        text = text.lower()
        # Replace spaces and underscores with hyphens
        text = text.replace(' ', '-').replace('_', '-')
        # Replace sequences of non-alphanumeric characters (excluding hyphens) with a single hyphen
        text = re.sub(r'[^a-z0-9-]+', '-', text)
        # Remove consecutive hyphens
        while '--' in text:
            text = text.replace('--', '-')
        # Remove leading/trailing hyphens
        text = text.strip('-')
        return text

    @staticmethod
    def camel_case_to_underscore(text):
        """Convert camelCase to snake_case"""
        if not text:
            return ""
        result = []
        for i, c in enumerate(text):
            if c.isupper() and i > 0:
                result.append('_')
            result.append(c.lower())
        return ''.join(result)

    @staticmethod
    def trim_whitespace(text):
        """Clean up whitespace in string"""
        if not text:
            return ""
        # Replace all whitespace with single space
        text = ' '.join(text.split())
        return text.strip()


    @staticmethod
    def to_dash_case(plugin_name, separator = '-'):
        """Converts CamelCase, PascalCase, or snake_case to dash-case (or other separator)."""
        if not plugin_name:
            return ""
        # Handle CamelCase/PascalCase: insert space before uppercase, then lowercase
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1 \2', plugin_name)
        s2 = re.sub('([a-z0-9])([A-Z])', r'\1 \2', s1).lower()
        # Replace spaces and underscores with the separator
        s3 = s2.replace(' ', separator).replace('_', separator)
        # Remove consecutive separators
        while f'{separator}{separator}' in s3:
             s3 = s3.replace(f'{separator}{separator}', separator)
        return s3.strip(separator)
    
    @staticmethod
    def normalize_plugin_name(plugin_name):
        """
        Removes the vendor prefix from a PascalCase plugin name by splitting into segments.
        If more than one segment is found, the first is removed.
        Segmentation occurs before uppercase letters that follow lowercase letters,
        or before the start of a word following an acronym.
        Example: VendorPluginName -> PluginName
        Example: TopdataMyFancyPluginSW6 -> MyFancyPluginSW6
        Example: VENDORPlugin -> Plugin
        Example: PluginName -> Name (Note: This might conflict with specific test expectations)
        """
        if not plugin_name or not plugin_name[0].isupper():
            return plugin_name # Return as is if empty or not starting with uppercase

        # Use regex to find segment boundaries
        # - (?<=[a-z])(?=[A-Z]): Positive lookbehind for lowercase, positive lookahead for uppercase (e.g., Plugin|Name)
        # - (?<=[A-Z])(?=[A-Z][a-z]): Positive lookbehind for uppercase, positive lookahead for uppercase followed by lowercase (e.g., VENDOR|Plugin)
        segments = re.split(r'(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])', plugin_name)

        # If more than one segment is found, assume the first is the vendor and remove it.
        if len(segments) > 1:
            return "".join(segments[1:])
        else:
            # Otherwise, return the original name (single segment).
            return plugin_name


    @staticmethod
    def to_title_case(text):
        """
        Converts PascalCase or camelCase text to Title Case with spaces.
        Handles acronyms like SW6 correctly.
        Example: MyFancyPluginSW6 -> My Fancy Plugin SW6
        Example: camelCaseText -> Camel Case Text
        """
        if not text:
            return ""
        result = []
        # Handle potential camelCase by capitalizing the first letter
        processed_text = text[0].upper() + text[1:] if text else ""

        for i, char in enumerate(processed_text):
            # Add space before uppercase letter if:
            # 1. It's not the first character (i > 0)
            # 2. The previous character is lowercase (detects word boundary like 'FancyPlugin')
            # 3. Or, the next character is lowercase (detects end of acronym like 'SW6Plugin')
            #    and the previous character is not already a space.
            if i > 0 and char.isupper():
                prev_char_is_lower = processed_text[i-1].islower()
                next_char_is_lower = (i + 1 < len(processed_text)) and processed_text[i+1].islower()
                prev_char_is_not_space = processed_text[i-1] != ' '

                if prev_char_is_lower or (next_char_is_lower and prev_char_is_not_space):
                     result.append(' ')
            result.append(char)
        # Join and potentially clean up multiple spaces if any edge cases create them
        return " ".join("".join(result).split())
