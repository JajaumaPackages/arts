# Makefile for source rpm: arts
# $Id$
NAME := arts
SPECFILE = $(firstword $(wildcard *.spec))

include ../common/Makefile.common
