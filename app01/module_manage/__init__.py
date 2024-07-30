#!/usr/bin/env python
# -*- coding:utf-8 -*-
from django.db import models
from datetime import datetime
import copy
from django.utils.safestring import mark_safe
from django.core.validators import ValidationError
from django import forms
from django.shortcuts import render, HttpResponse, redirect
import hashlib
from django.conf import settings
