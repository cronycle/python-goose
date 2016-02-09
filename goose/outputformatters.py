# -*- coding: utf-8 -*-
"""\
This is a python port of "Goose" orignialy licensed to Gravity.com
under one or more contributor license agreements.  See the NOTICE file
distributed with this work for additional information
regarding copyright ownership.

Python port was written by Xavier Grangier for Recrutae

Gravity.com licenses this file
to you under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance
with the License.  You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from HTMLParser import HTMLParser
from cleaners import OutputFormatterCleaner


class OutputFormatter(object):

    def __init__(self, config, article):
        # config
        self.config = config

        # article
        self.article = article

        # parser
        self.parser = self.config.get_parser()

        # stopwords class
        self.stopwords_class = config.stopwords_class

        # top node
        self.top_node = None

    def content_html(self, should_perform_processing=True):
        self.top_node = self.article.top_node

        if should_perform_processing:
            self.remove_negativescores_nodes()

        return OutputFormatterCleaner().clean(self.top_node)

    def remove_negativescores_nodes(self):
        """\
        if there are elements inside our top node
        that have a negative gravity score,
        let's give em the boot
        """
        gravity_items = self.parser.css_select(self.top_node, "*[gravityScore]")
        for item in gravity_items:
            score = self.parser.getAttribute(item, 'gravityScore')
            score = int(score, 0)
            if score < 1:
                item.getparent().remove(item)


class StandardOutputFormatter(OutputFormatter):
    pass
