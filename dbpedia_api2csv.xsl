<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet
    version = "1.0"
    xmlns:xsl   = "http://www.w3.org/1999/XSL/Transform"
    xmlns:fn    = "http://www.w3.org/2005/xpath-functions"
    xmlns:dbp   = "http://lookup.dbpedia.org/"
    xmlns       = "http://lookup.dbpedia.org/"
>

<xsl:output method="text" encoding="UTF-8" />

<xsl:template match="/">
    <xsl:apply-templates select="dbp:ArrayOfResult/dbp:Result"/>
</xsl:template>

<xsl:template match="dbp:Result">
    <xsl:apply-templates select="dbp:Label"/>
    <xsl:text>,</xsl:text>
    <xsl:apply-templates select="dbp:URI"/>
    <xsl:text>,</xsl:text>
    <xsl:apply-templates select="dbp:Description"/>
    <xsl:text>&#x0A;</xsl:text>
</xsl:template>

<xsl:template match="dbp:Label|dbp:URI|dbp:Description">"<xsl:value-of select="."/>"</xsl:template>


</xsl:stylesheet>
