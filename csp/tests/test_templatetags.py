from csp.tests.utils import ScriptTagTestBase


class TestDjangoTemplateTag(ScriptTagTestBase):

    def test_script_tag_injects_nonce(self):
        tpl = """
            {% load csp %}
            {% script %}var hello='world';{% endscript %}"""

        expected = """<script nonce="{}">var hello='world';</script>"""

        self.assert_template_eq(*self.process_templates(tpl, expected))

    def test_script_with_src_ignores_body(self):
        tpl = ("""
            {% load csp %}
            {% script src="foo" %}
                var hello='world';
            {% endscript %}""")

        expected = """<script nonce="{}" src="foo"></script>"""

        self.assert_template_eq(*self.process_templates(tpl, expected))

    def test_script_tag_sets_attrs_correctly(self):
        tpl = """
            {% load csp %}
            {% script type="application/javascript" id="jeff" defer=True%}
                var hello='world';
            {% endscript %}"""

        expected = (
            '<script'
            ' nonce="{}" id="jeff" type="application/javascript" defer>'
            'var hello=\'world\';</script>')

        self.assert_template_eq(*self.process_templates(tpl, expected))

    def test_async_attribute_with_falsey(self):
        tpl = """
            {% load csp %}
            {% script src="foo.com/bar.js" async=False %}
            {% endscript %}"""

        expected = ('<script nonce="{}" src="foo.com/bar.js" async=false>'
                    '</script>')

        self.assert_template_eq(*self.process_templates(tpl, expected))

    def test_async_attribute_with_truthy(self):
        tpl = """
            {% load csp %}
            {% script src="foo.com/bar.js" async=True %}
                var hello='world';
            {% endscript %}"""

        expected = '<script nonce="{}" src="foo.com/bar.js" async></script>'

        self.assert_template_eq(*self.process_templates(tpl, expected))

    def test_nested_script_tags_are_removed(self):
        """Lets end users wrap their code in script tags for the sake of their
           development environment"""
        tpl = """
            {% load csp %}
            {% script type="application/javascript" id="jeff" defer=True%}
                <script type="text/javascript">
                var hello='world';
                </script>
            {% endscript %}"""

        expected = (
            '<script'
            ' nonce="{}" id="jeff" type="application/javascript" defer>'
            'var hello=\'world\';</script>')

        self.assert_template_eq(*self.process_templates(tpl, expected))
