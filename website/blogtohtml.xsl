<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet
    version = "1.0"
    xmlns:xsl   = "http://www.w3.org/1999/XSL/Transform"
    xmlns:fn    = "http://www.w3.org/2005/xpath-functions"
    xmlns:ft    = "http://www.andonyar.com/rec/2012/sempipe/fresnelxml"
    xmlns:xhtml = "http://www.w3.org/1999/xhtml"
    xmlns       = "http://www.w3.org/1999/xhtml"
    exclude-result-prefixes="xsl fn ft xhtml"
>

<xsl:import href="file:///home/urs/p/sempipe/transforms/fresneltoxhtml5.xsl"/>

<xsl:template match="ft:resource[contains(ft:format/@class, 'Post')]">
    <!-- Note that this is inside a section with a title due to the
         value it is contained in. -->
    <p style="text-align: right">
        <xsl:apply-templates select="ft:property[contains(ft:format/@class, 'meta')]"/>
    </p>
    <xsl:apply-templates select="ft:property[not(contains(ft:format/@class, 'meta'))]"/>
</xsl:template>

</xsl:stylesheet>
