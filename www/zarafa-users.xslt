<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="html" indent="yes" omit-xml-declaration="yes" />
<xsl:param name="columns" select="2"/>
<xsl:param name="sort" select="'username'"/>

<xsl:template match="/zarafaadmin/error">
  <table align="center">
    <caption style="color:red">An Error occurred, Please contact your System Administrator</caption>
    <tr>
      <td align="right" style="color:red">Error Number:</td>
      <td align="left"><xsl:value-of select="@code"/></td>
    </tr>
    <tr>
      <td align="right" style="color:red">Error Message:</td>
      <td align="left"><xsl:value-of select="@msg"/></td>
    </tr>
    <tr>
      <td align="right" style="color:red">Original Command:</td>
      <td align="left"><xsl:value-of select="@cmd"/></td>
    </tr>
  </table>
</xsl:template>

<xsl:template match="/zarafaadmin/users">
  <pre>
    <xsl:choose>
    <xsl:when test="count(user) = 1">
      <table id="zarafa-user">
        <tr><th colspan="6" align="center">User Detail for <xsl:value-of select="user/@username"/></th></tr>
        <tr><th colspan="3" align="center">Zarafa Details</th><th colspan="3" align="center">LDAP Details</th></tr>
        <tr class="hover">
          <td>&#xA0;</td>
          <th align="right">Username:&#xA0;</th><td><xsl:value-of select="user/@username"/></td>
          <td>&#xA0;</td>          
          <th align="right">GivenName:&#xA0;</th><td><xsl:value-of select="user/@pr_given_name"/></td>
        </tr>
        <tr class="hover">
          <td>&#xA0;</td>          
          <th align="right">Email:&#xA0;</th><td><xsl:value-of select="user/@emailaddress"/></td>
          <td>&#xA0;</td>          
          <th align="right">Surname:&#xA0;</th><td><xsl:value-of select="user/@pr_surname"/></td>
        </tr>
        <tr class="hover">
          <td>&#xA0;</td>          
          <th align="right">Active:&#xA0;</th><td><xsl:if test="user/@active = 'yes'">&#x2713;</xsl:if></td>
          <td>&#xA0;</td>          
          <th align="right">Fullname:&#xA0;</th><td><xsl:value-of select="user/@fullname"/></td>
        </tr>
        <tr class="hover">
          <td>&#xA0;</td>          
          <th align="right">Administrator:&#xA0;</th><td><xsl:if test="user/@administrator = 'yes'">&#x2713;</xsl:if></td>
          <td>&#xA0;</td>          
          <th align="right">Title:&#xA0;</th><td><xsl:value-of select="user/@pr_title"/></td>
        </tr>
        <tr class="hover">
          <td>&#xA0;</td>          
          <th align="right">Visible:&#xA0;</th><td><xsl:if test="user/@addressbook = 'Visible'">&#x2713;</xsl:if></td>
          <td>&#xA0;</td>          
          <th align="right">Section:&#xA0;</th><td><xsl:value-of select="user/@pr_department_name"/></td>
        </tr>
        <tr class="hover">
          <td>&#xA0;</td>          
          <th align="right">Auto-accept:&#xA0;</th><td><xsl:if test="user/@autoacceptmeetingreq = 'yes'">&#x2713;</xsl:if></td>
          <td>&#xA0;</td>          
          <th align="right">Location:&#xA0;</th><td><xsl:value-of select="user/@location"/></td>
        </tr>
        <tr class="hover">
          <td>&#xA0;</td>          
          <th align="right">Logon:&#xA0;</th>
          <td>
            <xsl:if test="user/logon/@lag &gt;= 30">
              <xsl:attribute name="class">red</xsl:attribute>
            </xsl:if>   
            <xsl:value-of select="user/logon/@date"/>
          </td>
          <td>&#xA0;</td>          
          <th align="right">Telephone:&#xA0;</th><td><xsl:value-of select="user/@pr_business_telephone_number"/></td>
        </tr>
        <tr class="hover">
          <td>&#xA0;</td>          
          <th align="right">Logoff:&#xA0;</th>
          <td>
            <xsl:if test="user/logoff/@lag &gt;= 30">
              <xsl:attribute name="class">red</xsl:attribute>
            </xsl:if>  
            <xsl:value-of select="user/logoff/@date"/>
          </td>
          <td>&#xA0;</td>          
          <th align="right">Mobile:&#xA0;</th><td><xsl:value-of select="user/@pr_mobile_telephone_number"/></td>
        </tr>
        <tr class="hover">
          <td colspan="4">&#xA0;</td>
          <th align="right">Fax:&#xA0;</th><td><xsl:value-of select="user/@pr_business_fax_number"/></td>
        </tr>
      </table>

      <table id="zarafa-user-quota">
        <tr><th colspan="6" class="center">Quota Information<xsl:if test="user/@quotaoverrides = 'yes'">&#xA0;(Override Defaults &#x2713;)</xsl:if></th></tr>
        <tr class="hover">
          <td>&#xA0;</td>          
          <th align="right">Warning Level:&#xA0;</th><td><xsl:value-of select="format-number(user/@quotawarn div 1024,'###,###,##0')"/> MB</td>
          <td>&#xA0;</td>          
          <th align="right">Soft Level:&#xA0;</th><td><xsl:value-of select="format-number(user/@quotasoft div 1024,'###,###,##0')"/> MB</td>         
        </tr>
        <tr class="hover">
          <td>&#xA0;</td>          
          <th align="right">Hard Level:&#xA0;</th><td><xsl:value-of select="format-number(user/@quotahard div 1024,'###,###,##0')"/> MB</td>
          <td>&#xA0;</td>          
          <th align="right">Current Size:&#xA0;</th>
          <td>
            <xsl:choose>
            <xsl:when test="number(user/@size div 1024) &gt;= number(user/@quotahard)">
              <xsl:attribute name="class">hard</xsl:attribute>
            </xsl:when>
            <xsl:when test="number(user/@size div 1024) &gt;= number(user/@quotasoft)">
              <xsl:attribute name="class">soft</xsl:attribute>
            </xsl:when>
            <xsl:when test="number(user/@size div 1024) &gt;= number(user/@quotawarn)">
              <xsl:attribute name="class">warn</xsl:attribute>
            </xsl:when>
            </xsl:choose>
            <xsl:value-of select="format-number(user/@size div 1048576,'###,###,##0.00')"/> MB
          </td>
        </tr>

        <tr><td colspan="6">&#xA0;</td></tr>
        <tr>
          <th colspan="6" class="center">Send As Rights
            <xsl:if test="count(user/sendas) &gt; 0">
              (<xsl:value-of select="user/sendas"/>)
            </xsl:if>
          </th>
        </tr>



        <xsl:if test="count(user/sendas) &gt; 0">
          <tr>
            <th colspan="3" align="right" valign="top">Send As Rights:&#xA0;</th>
            <td>&#xA0;</td>            
            <td colspan="2">
              <xsl:for-each select="user/sendas"><xsl:sort select="translate(@username, 'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')" order="ascending" />
              <a href="./zarafa-users.php?user={@username}"><xsl:value-of select="@username"/></a><br/>
              </xsl:for-each>
            </td>
          </tr>
        </xsl:if>



        <tr><td colspan="6">&#xA0;</td></tr>
        <tr>
          <th colspan="6" class="center">Groups
            <xsl:if test="count(user/group) &gt; 0">
              (<xsl:value-of select="user/group"/>)
            </xsl:if>
          </th>
        </tr>

        <xsl:if test="count(user/group) &gt; 0">
          <tr>
            <th colspan="3" align="right" valign="top">Groups:&#xA0;</th>
            <td>&#xA0;</td>            
            <td colspan="2">
              <xsl:for-each select="user/group"><xsl:sort select="translate(@groupname, 'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')" order="ascending" />
              <a href="./zarafa-groups.php?group={@groupname}"><xsl:value-of select="@groupname"/></a><br/>
              </xsl:for-each>
            </td>
          </tr>
        </xsl:if>
      </table>
    </xsl:when>

    <xsl:otherwise>
      <table id="zarafa-users">
      <tr>
        <th align="left"><a href="./zarafa-users.php?sort=username">Username</a></th>
        <th align="left"><a href="./zarafa-users.php?sort=fullname">Full Name</a></th>
        <th align="left"><a href="./zarafa-users.php?sort=emailaddress">Email Address</a></th>
        <th align="right"><a href="./zarafa-users.php?sort=quotawarn">Warning</a></th>
        <th align="right"><a href="./zarafa-users.php?sort=quotasoft">Soft</a></th>
        <th align="right"><a href="./zarafa-users.php?sort=quotahard">Hard</a></th>
        <th align="right"><a href="./zarafa-users.php?sort=size">Size (MB)</a></th>
        <th align="center"><a href="./zarafa-users.php?sort=logon">Last Logon</a></th>
      </tr>
      <xsl:choose>
      <xsl:when test="$sort = 'fullname'">
        <xsl:apply-templates select="user"><xsl:sort select="translate(@fullname, 'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')" order="ascending" /></xsl:apply-templates>
      </xsl:when>
      <xsl:when test="$sort = 'emailaddress'">
        <xsl:apply-templates select="user"><xsl:sort select="translate(@emailaddress, 'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')" order="ascending" /></xsl:apply-templates>
      </xsl:when>
      <xsl:when test="$sort = 'quotawarn'">
        <xsl:apply-templates select="user"><xsl:sort select="@quotawarn" order="descending" data-type="number"/></xsl:apply-templates>
      </xsl:when>
      <xsl:when test="$sort = 'quotasoft'">
        <xsl:apply-templates select="user"><xsl:sort select="@quotasoft" order="descending" data-type="number"/></xsl:apply-templates>
      </xsl:when>
      <xsl:when test="$sort = 'quotahard'">
        <xsl:apply-templates select="user"><xsl:sort select="@quotahard" order="descending" data-type="number"/></xsl:apply-templates>
      </xsl:when>
      <xsl:when test="$sort = 'size'">
        <xsl:apply-templates select="user"><xsl:sort select="@size" order="descending" data-type="number"/></xsl:apply-templates>
      </xsl:when>
      <xsl:when test="$sort = 'logon'">
        <xsl:apply-templates select="user"><xsl:sort select="logon/@lag" order="descending" data-type="number"/></xsl:apply-templates>
      </xsl:when>
      <xsl:otherwise>
        <xsl:apply-templates select="user"><xsl:sort select="translate(@username, 'abcdefghijklmnopqrstuvwxyz','ABCDEFGHIJKLMNOPQRSTUVWXYZ')" order="ascending" /></xsl:apply-templates>
      </xsl:otherwise>
      </xsl:choose>
      </table>
    </xsl:otherwise>
    </xsl:choose>
  </pre>
</xsl:template>

<xsl:template match="user">
  <tr class="entry">
  <td><a href="./zarafa-users.php?user={@username}"><xsl:value-of select="@username"/></a></td>
  <td><xsl:value-of select="@fullname"/></td>
  <td><xsl:value-of select="@emailaddress"/></td>
  <td class="number"><xsl:value-of select="format-number(@quotawarn div 1024,'###,###,##0')"/></td>
  <td class="number"><xsl:value-of select="format-number(@quotasoft div 1024,'###,###,##0')"/></td>
  <td class="number"><xsl:value-of select="format-number(@quotahard div 1024,'###,###,##0')"/></td>

  <td>
    <xsl:choose>
    <xsl:when test="number(@size div 1024) &gt;= number(@quotahard)">
      <xsl:attribute name="class">number hard</xsl:attribute>
    </xsl:when>
    <xsl:when test="number(@size div 1024) &gt;= number(@quotasoft)">
      <xsl:attribute name="class">number soft</xsl:attribute>
    </xsl:when>
    <xsl:when test="number(@size div 1024) &gt;= number(@quotawarn)">
      <xsl:attribute name="class">number warn</xsl:attribute>
    </xsl:when>
    <xsl:otherwise>
      <xsl:attribute name="class">number</xsl:attribute>
    </xsl:otherwise>
    </xsl:choose>
  <xsl:value-of select="format-number(@size div 1048576,'###,###,##0.00')"/></td>

  <td align="center">
    <xsl:if test="logon/@lag &gt;= 30">
      <xsl:attribute name="class">red</xsl:attribute>
    </xsl:if>   
    <xsl:value-of select="logon/@date"/></td>
  </tr>
</xsl:template>

</xsl:stylesheet>