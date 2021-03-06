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
import os
import json
import hashlib
import unittest

from base import MockResponse
from extractors import TestExtractionBase

from goose.configuration import Configuration
from goose.images.image import Image
from goose.utils import FileHelper

CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))


class MockResponseImage(MockResponse):

    def image_content(self, req):
        md5_hash = hashlib.md5(req.get_full_url()).hexdigest()
        current_test = self.cls._get_current_testname()
        path = os.path.join(CURRENT_PATH, "data", "images", current_test, md5_hash)
        path = os.path.abspath(path)
        f = open(path, 'rb')
        content = f.read()
        f.close()
        return content

    def html_content(self, req):
        current_test = self.cls._get_current_testname()
        path = os.path.join(CURRENT_PATH, "data", "images", current_test, "%s.html" % current_test)
        path = os.path.abspath(path)
        return FileHelper.loadResourceFile(path)

    def content(self, req):
        if self.cls.data['url'] == req.get_full_url():
            return self.html_content(req)
        return self.image_content(req)


class ImageExtractionTests(TestExtractionBase):
    """\
    Base Mock test case
    """
    callback = MockResponseImage

    def loadData(self):
        """\

        """
        suite, module, cls, func = self.id().split('.')
        path = os.path.join(CURRENT_PATH, "data", module, func, "%s.json" % func)
        path = os.path.abspath(path)
        content = FileHelper.loadResourceFile(path)
        self.data = json.loads(content)

    def getConfig(self):
        config = Configuration()
        config.enable_image_fetching = True
        return config

    def getExpectedImage(self, expected_value):
        image = Image()
        for k, v in expected_value.items():
            setattr(image, k, v)
        return image

    def assert_images(self, fields, expected_values, result_images):
        for expected_value in expected_values:
            if expected_value['src'] == '':
                continue

            result_image = None
            for result_image_candidate in result_images:
                if result_image_candidate.src == expected_value['src']:
                    result_image = result_image_candidate

            msg = u"Result value is not a Goose Image instance"
            self.assertTrue(isinstance(result_image, Image), msg=msg)

            # expected image
            expected_image = self.getExpectedImage(expected_value)
            msg = u"Expected value is not a Goose Image instance"
            self.assertTrue(isinstance(expected_image, Image), msg=msg)

            # check
            msg = u"Returned Image is not the one expected"
            self.assertEqual(expected_image.src, result_image.src, msg=msg)

            fields = vars(expected_image)
            for k, v in fields.items():
                msg = u"Returned Image attribute %s is not the one expected" % k
                self.assertEqual(getattr(expected_image, k), getattr(result_image, k), msg=msg)

    def test_basic_images(self):
        article = self.getArticle()
        fields = ['images']
        self.runArticleAssertions(article=article, fields=fields)

    def _test_known_images_css(self, article):
        # check if we have an image in article.top_node
        images = self.parser.getElementsByTag(article.top_node,  tag='img')
        self.assertEqual(len(images), 0)

        # we dont' have an image in article.top_node
        # check if the correct image was retrieved
        fields = ['images']
        self.runArticleAssertions(article=article, fields=fields)

    def test_known_images_empty_src(self):
        'Tests that img tags for known image sources with empty src attributes are skipped.'
        article = self.getArticle()
        self._test_known_images_css(article)

    def test_opengraph_tag(self):
        article = self.getArticle()
        self._test_known_images_css(article)

    def test_image_sizes(self):
        article = self.getArticle()
        fields = ['images']
        self.runArticleAssertions(article=article, fields=fields)
