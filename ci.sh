#!/bin/bash

uvx ruff check
uvx ruff format --check
uvx ty check
