//\////////////////////////////////
//\  overLIB 3.33  --  This notice must remain untouched at all times.
//\  Copyright Erik Bosrup 1998-2001. All rights reserved.
//\
//\  By Erik Bosrup (erik@bosrup.com).  Last modified 2001-01-26.
//\  Portions by Dan Steinman (dansteinman.com). Additions by other people are
//\  listed on the overLIB homepage.
//\
//\  Get the latest version at http://www.bosrup.com/web/overlib/
//\
//\  This script is published under an open source license. Please read the license
//\  agreement online at: http://www.bosrup.com/web/overlib/license.html
//\  If you have questions regarding the license please contact erik@bosrup.com.
//\
//\  This script library was originally created for personal use. By request it has
//\  later been made public. This is free software. Do not sell this as your own
//\  work, or remove this copyright notice. For full details on copying or changing
//\  this script please read the license agreement at the link above.
//\
//\  Please give credit on sites that use overLIB and submit changes of the script
//\  so other people can use them as well. This script is free to use, don't abuse.
//\////////////////////////////////
//\mini

//\////////////////////////////////
//\  ▸ the URLs above, at "bosrup.com", are dead: the entire site went belly-up.
//\////////////////////////////////


//\////////////////////////////////
//\  Thayer flavor:
//\  I've renamed "overlib" to "Ebox", "Fbox", etc.
//\  to save 3 characters on each call
//\  while specifying the language (English, French, etc.)
//\////////////////////////////////


////////////////////////////////////
// CONSTANTS
// Don't touch these. :)
////////////////////////////////////
var INARRAY		=	1;
var CAPARRAY		=	2;
var STICKY		=	3;
var BACKGROUND		=	4;
var NOCLOSE		=	5;
var CAPTION		=	6;
var LEFT		=	7;
var RIGHT		=	8;
var CENTER		=	9;
var OFFSETX		=	10;
var OFFSETY		=	11;
var FGCOLOR		=	12;
var BGCOLOR		=	13;
var TEXTCOLOR		=	14;
var CAPCOLOR		=	15;
var CLOSECOLOR		=	16;
var WIDTH		=	17;
var BORDER		=	18;
var STATUS		=	19;
var AUTOSTATUS		=	20;
var AUTOSTATUSCAP	=	21;
var HEIGHT		=	22;
var CLOSETEXT		=	23;
var SNAPX		=	24;
var SNAPY		=	25;
var FIXX		=	26;
var FIXY		=	27;
var FGBACKGROUND	=	28;
var BGBACKGROUND	=	29;
var PADX		=	30;
var PADY		=	31;
var PADX2		=	32;
var PADY2		=	33;
var FULLHTML		=	34;
var ABOVE		=	35;
var BELOW		=	36;
var CAPICON		=	37;
var TEXTFONT		=	38;
var CAPTIONFONT		=	39;
var CLOSEFONT		=	40;
var TEXTSIZE		=	41;
var CAPTIONSIZE		=	42;
var CLOSESIZE		=	43;
var FRAME		=	44;
var TIMEOUT		=	45;
var FUNCTION		=	46;
var DELAY		=	47;
var HAUTO		=	48;
var VAUTO		=	49;


////////////////////////////////////
// DEFAULT CONFIGURATION
// You don't have to change anything here if you don't want to. All of this can be
// changed on your html page or through an overLIB call.
////////////////////////////////////

// Main background color (the large area)
// Usually a bright color (white, yellow etc)
if (typeof ol_fgcolor == 'undefined') { var ol_fgcolor = "#FFFFDD";}
	
// Border color and color of caption
// Usually a dark color (black, brown etc)
if (typeof ol_bgcolor == 'undefined') { var ol_bgcolor = "#333399";}
	
// Text color
// Usually a dark color
if (typeof ol_textcolor == 'undefined') { var ol_textcolor = "#000066";}
	
// Color of the caption text
// Usually a bright color
if (typeof ol_capcolor == 'undefined') { var ol_capcolor = "#FFFFFF";}
	
// Color of "Close" when using Sticky
// Usually a semi-bright color
if (typeof ol_closecolor == 'undefined') { var ol_closecolor = "#9999FF";}

// Font face for the main text
if (typeof ol_textfont == 'undefined') { var ol_textfont = "Courier, Courier New, serif";}

// Font face for the caption
if (typeof ol_captionfont == 'undefined') { var ol_captionfont = "Courier, Courier New";}

// Font face for the close text
if (typeof ol_closefont == 'undefined') { var ol_closefont = "Courier, Courier New";}

// Font size for the main text
if (typeof ol_textsize == 'undefined') { var ol_textsize = "1";}

// Font size for the caption
if (typeof ol_captionsize == 'undefined') { var ol_captionsize = "1";}

// Font size for the close text
if (typeof ol_closesize == 'undefined') { var ol_closesize = "1";}

// Width of the popups in pixels
// 100-300 pixels is typical
if (typeof ol_width == 'undefined') { var ol_width = "225";}

// How thick the ol_border should be in pixels
// 1-3 pixels is typical
if (typeof ol_border == 'undefined') { var ol_border = "2";}

// How many pixels to the right/left of the cursor to show the popup
// Values between 3 and 12 are best
if (typeof ol_offsetx == 'undefined') { var ol_offsetx = 10;}
	
// How many pixels below the cursor to show the popup
// Values between 3 and 12 are best
if (typeof ol_offsety == 'undefined') { var ol_offsety = 10;}

// Default text for popups
// Should you forget to pass something to overLIB this will be displayed.
if (typeof ol_text == 'undefined (but the link is good !)') { var ol_text = "Default Text"; }

// Default caption
// You should leave this blank or you will have problems making non caps popups.
if (typeof ol_cap == 'undefined') { var ol_cap = ""; }

// Decides if sticky popups are default.
// 0 for non, 1 for stickies.
if (typeof ol_sticky == 'undefined') { var ol_sticky = 0; }

// Default background image. Better left empty unless you always want one.
if (typeof ol_background == 'undefined') { var ol_background = ""; }

// Text for the closing sticky popups.
// Normal is "Close".
if (typeof ol_close == 'undefined') { var ol_close = "Close"; }

// Default vertical alignment for popups.
// It's best to leave RIGHT here. Other options are LEFT and CENTER.
if (typeof ol_hpos == 'undefined') { var ol_hpos = RIGHT; }
// TO CHANGE THIS WITHIN A PAGE: see syntax on
//    E/Gazetteer/Places/Asia/Russia/_Topics/history/_Texts/SMANPS/Appendices/C*.html
// (search for "ol_hpos")

// Default status bar text when a popup is invoked.
if (typeof ol_status == 'undefined') { var ol_status = ""; }

// If the status bar automatically should load either text or caption.
// 0=nothing, 1=text, 2=caption
if (typeof ol_autostatus == 'undefined') { var ol_autostatus = 0; }

// Default height for popup. Often best left alone.
if (typeof ol_height == 'undefined') { var ol_height = -1; }

// Horizontal grid spacing that popups will snap to.
// 0 makes no grid, anything else will cause a snap to that grid spacing.
if (typeof ol_snapx == 'undefined') { var ol_snapx = 0; }

// Vertical grid spacing that popups will snap to.
// 0 makes no grid, anything else will cause a snap to that grid spacing.
if (typeof ol_snapy == 'undefined') { var ol_snapy = 0; }

// Sets the popups horizontal position to a fixed column.
// Anything above -1 will cause fixed position.
if (typeof ol_fixx == 'undefined') { var ol_fixx = -1; }

// Sets the popups vertical position to a fixed row.
// Anything above -1 will cause fixed position.
if (typeof ol_fixy == 'undefined') { var ol_fixy = -1; }

// Background image for the popups inside.
if (typeof ol_fgbackground == 'undefined') { var ol_fgbackground = ""; }

// Background image for the popups frame.
if (typeof ol_bgbackground == 'undefined') { var ol_bgbackground = ""; }

// How much horizontal left padding text should get by default when BACKGROUND is used.
if (typeof ol_padxl == 'undefined') { var ol_padxl = 1; }

// How much horizontal right padding text should get by default when BACKGROUND is used.
if (typeof ol_padxr == 'undefined') { var ol_padxr = 1; }

// How much vertical top padding text should get by default when BACKGROUND is used.
if (typeof ol_padyt == 'undefined') { var ol_padyt = 1; }

// How much vertical bottom padding text should get by default when BACKGROUND is used.
if (typeof ol_padyb == 'undefined') { var ol_padyb = 1; }

// If the user by default must supply all html for complete popup control.
// Set to 1 to activate, 0 otherwise.
if (typeof ol_fullhtml == 'undefined') { var ol_fullhtml = 0; }

// Default vertical position of the popup. Default should normally be BELOW.
// ABOVE only works when HEIGHT is defined.
if (typeof ol_vpos == 'undefined') { var ol_vpos = BELOW; }

// Default height of popup to use when placing the popup above the cursor.
if (typeof ol_aboveheight == 'undefined') { var ol_aboveheight = 50; }

// Default icon to place next to the popups caption.
if (typeof ol_caption == 'undefined') { var ol_capicon = ""; }

// Default frame. We default to current frame if there is no frame defined.
if (typeof ol_frame == 'undefined') { var ol_frame = self; }

// Default timeout. By default there is no timeout.
if (typeof ol_timeout == 'undefined') { var ol_timeout = 0; }

// Default javascript function. By default there is none.
if (typeof ol_function == 'undefined') { var ol_function = Function(); }

// Default timeout. By default there is no timeout.
if (typeof ol_delay == 'undefined') { var ol_delay = 0; }

// If overLIB should decide the horizontal placement.
if (typeof ol_hauto == 'undefined') { var ol_hauto = 0; }

// If overLIB should decide the vertical placement.
if (typeof ol_vauto == 'undefined') { var ol_vauto = 0; }


////////////////////////////////////
// ARRAY CONFIGURATION
// You don't have to change anything here if you don't want to. The following
// arrays can be filled with text and html if you don't wish to pass it from
// your html page.
////////////////////////////////////

// THAYER'S BOILERPLATES:
//\////////////////////////////////
//\  Thayer CONSTANTS:
//\////////////////////////////////

var CarelessLoeb50	=	"<CENTER>The Loeb edition —<BR>thru 50 years of reprintings! —<BR>has <SPAN CLASS=goof>";
var CarelessLoeb60	=	"<CENTER>The Loeb edition —<BR>thru 60 years of reprintings! —<BR>has <SPAN CLASS=goof>";
var CarelessLoeb70	=	"<CENTER>The Loeb edition —<BR>thru 70 years of reprintings! —<BR>has <SPAN CLASS=goof>";
var CarelessLoeb80	=	"<CENTER>The Loeb edition —<BR>thru 80 years of reprintings! —<BR>has <SPAN CLASS=goof>";
var CarelessLoeb90	=	"<CENTER>The Loeb edition —<BR>thru 90 years of reprintings! —<BR>has <SPAN CLASS=goof>";
var CarelessLoebX	=	"<CENTER>The Loeb edition —<BR>thru many years of reprintings! —<BR>has <SPAN CLASS=goof>";
var Cullum0	=	":<BR>This is a link<BR>to another entry<BR>in Cullum\'s Register.<BR>(<SPAN CLASS=alert>Opens in THIS window</SPAN>)</CENTER>";
var Cullum1	=	"<CENTER>USMA, Class of ";
var Cullum2	=	":<BR>This is a link to the<BR>biographical summary<BR>in Cullum\'s Register.<BR><SPAN CLASS=whole>(Opens in another window)</SPAN></CENTER>";
var CullumR1 = "<P CLASS=center><B>CLASS RANK</B><BR>— of ";
var CullumR2 = " in the Class";


// ENGLISH:
var Eng2		=	"<BR><SPAN CLASS=whole><I>(English, opens in another window)</I></SPAN>";
var EngSearch	=	"<BR>then search for<BR><SPAN CLASS=searchand>";


// FRENCH:
// var Fr0	=	"<P CLASS=center><SPAN CLASS=alert><I>(La page s\'ouvre dans CETTE fenêtre)</I></SPAN>";
// var Fr1	=	"<P CLASS=center><I>(La page s\'ouvre dans une autre fenêtre)</I>";
// var Fr2	=	"<P CLASS=center><I>Le lien est hors site :<BR>la page s\'ouvre<BR>dans une autre fenêtre</I>";
// var Fr5	=	"<P CLASS=center><I>(Ailleurs sur cette page)</I>";
// var FrGk2		=	"<BR><I>(<SPAN CLASS=transcribed_Greek>Grec</SPAN> s\'ouvre dans une autre fenêtre)</I>";
// var FrGkSearch	=	"<BR>puis chercher<BR><SPAN CLASS=searchandGreek>";
// var FrLat2		=	"<BR><I>(<SPAN CLASS=Latin>Latin</SPAN>, s\'ouvre dans une autre fenêtre)</I>";
// var FrLatSearch	=	"<BR>puis chercher<BR><SPAN CLASS=searchandLatin>";


// GREEK:
var Gk2		=	"<BR><I>(<SPAN CLASS=transcribed_Greek>Greek</SPAN>, opens in another window)</I>";
var GkSearch	=	"<BR>then search for<BR><SPAN CLASS=searchandGreek>";


// ITALIAN:
var It5 = "<P CLASS=center><I>(Altrove su questa pagina)</I>";
var ItGk2		=	"<BR><I>(in <SPAN CLASS=transcribed_Greek>Greco</SPAN>, apre in un altro pannello)</I>";
var ItGkSearch	=	"<BR>poi cercare<BR><SPAN CLASS=searchandGreek>";
var ItLat2		=	"<BR><I>(in <SPAN CLASS=Latin>Latino</SPAN>, apre in un altro pannello)</I>";
var ItLatSearch	=	"<BR>poi cercare<BR><SPAN CLASS=searchandLatin>";


// LATIN:
var Lat2		=	"<BR><I>(<SPAN CLASS=Latin>Latin</SPAN>, opens in another window)</I>";
var LatSearch	=	"<BR>then search for<BR><SPAN CLASS=searchandLatin>";
var RedSearch	=	"<BR>then search for the word or passage in <SPAN CLASS=red>red</SPAN>";


// SPANISH:
var SpGk2		=	"<BR><I>(<SPAN CLASS=transcribed_Greek>Griego</SPAN>, abre en una otra ventana)</I>";
var SpGkSearch	=	"<BR>pues buscar<BR><SPAN CLASS=searchandGreek>";
var SpLat2		=	"<BR><I>(<SPAN CLASS=Latin>Latín</SPAN>, abre en una otra ventana)</I>";
var SpLatSearch	=	"<BR>pues buscar<BR><SPAN CLASS=searchandLatin>";


var CClickHere = "<P CLASS=center>Feu clic aquí per<BR>";
var EClickHere = "<P CLASS=center>Click here for<BR>";
var FClickHere = "<P CLASS=center>Faire clic ici pour<BR>";
var IClickHere = "<P CLASS=center>Cliccare qui per<BR>";
var NClickHere = "<P CLASS=center>Klik hier voor<BR>";
var PClickHere = "<P CLASS=center>Clique aqui para<BR>";
var SClickHere = "<P CLASS=center>Haga clic aquí para<BR>";
var CZero = "<P CLASS=center><SPAN CLASS=alert>La pàgina s\'obre en<BR>AQUESTA finestra</SPAN>";
var EZero = "<P CLASS=center><SPAN CLASS=alert>Page opens<BR>in THIS window</SPAN>";
var FZero = "<P CLASS=center><SPAN CLASS=alert>S\'ouvre dans<BR>CETTE fenêtre</SPAN>";
var IZero = "<P CLASS=center><SPAN CLASS=alert>Si apre in<BR>QUESTO pannello</SPAN>";
var PZero = "<P CLASS=center><SPAN CLASS=alert>A página abre<BR>NESTA janela</SPAN>";
var SZero = "<P CLASS=center><SPAN CLASS=alert>La página abre<BR>en ESTA ventana</SPAN>";
var CThisWindow = "<BR><SPAN CLASS=alert>La pàgina s\'obre<BR>en AQUESTA finestra</SPAN>";
var EThisWindow = "<BR><SPAN CLASS=alert>Page opens<BR>in THIS window</SPAN>";
var FThisWindow = "<BR><SPAN CLASS=alert>S\'ouvre dans<BR>CETTE fenêtre</SPAN>";
var IThisWindow = "<BR><SPAN CLASS=alert>Si apre in<BR>QUESTO pannello</SPAN>";









// THAYER'S ARRAYS:
// Array with texts. FOR SIMPLICITY, KEEP THIS AT LINE 350 (Number is then linenum minus 355)
// LANGUAGE ORDER: E:0 - F:10 - I:20 - L:30 - S:40 - P:90 (…0-4: EFILS)
// AFTER THE COMMA AT THE END OF EACH LINE: THERE MUST BE A SPACE!
// EXCEPT THE LAST LINE HAS NO COMMA, NO SPACE: FOR SIMPLICITY, KEEP IT AS A BLANK LINE.
var ol_texts = new Array(//START ARRAY; end is at END ARRAY
EZero, 
"<P CLASS=center><I>(Page opens in another window)</I>", 
"<P CLASS=center><I>Link is offsite:<BR>page opens in<BR>another window.</I>", 
"<P CLASS=center><I>(This photo or a related one, opens in another window)</I>", 
"<P CLASS=center><I>(The photo will open in another window)</I>", 
"<P CLASS=center><I>(Elsewhere on this page)</I>", 
EClickHere+"the author\'s note at the bottom of this page.", 
EClickHere+"my note at the bottom of this page.", 
"<P CLASS=center>Click here<BR>to go back<BR>to the reference<BR>in the text.", 
"<P CLASS=center>If you don\'t know what this is about,<BR>the explanation is only a click away.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FZero, 
"<P CLASS=center><I>(La page s\'ouvre dans une autre fenêtre)</I>", 
"<P CLASS=center><I>Le lien est hors site :<BR>la page s\'ouvre<BR>dans une autre fenêtre</I>", 
"<P CLASS=center><I>(Cette photo ou une photo apparentée, s\'ouvre dans une autre fenêtre)</I>", 
"<P CLASS=center><I>(Cette photo s\'ouvre dans une autre fenêtre)</I>", 
"<P CLASS=center><I>(Ailleurs sur cette page)</I>", 
FClickHere+"la note de l\'auteur au bas de la page.", 
FClickHere+"ma note<BR>au bas de la page.", 
FClickHere+"retourner au renvoi dans le texte.", 
"<P CLASS=center>Si vous ne savez pas ce de quoi il s\'agit, il n\'y a qu\'à faire clic pour l\'explication.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
"<P CLASS=center><SPAN CLASS=alert>(Die Seite öffnet sich in DIESEM Fenster)</SPAN>", 
"<P CLASS=center><I>(Die Seite öffnet sich in einem anderen Fenster)</I>", 
"<P CLASS=center><I>(Auf externe Site: die Seite öffnet sich in einem anderen Fenster)</I>", 
"<P CLASS=center><I>(Dieses Foto oder ein Ähnliches Foto öffnet sich in einem anderen Fenster)</I>", 
"<P CLASS=center><I>(Die Foto öffnet sich in einem anderen Fenster)</I>", 
" ", 
" ", 
" ", 
" ", 
" ", 
IZero, 
"<P CLASS=center><I>(La pagina si apre in un altro pannello)</I>", 
"<P CLASS=center><I>Il link è fuori sito:<BR>la pagina si apre<BR>in un altro pannello</I>", 
"<P CLASS=center><I>(Questa foto o una foto connessa, si apre in un altro pannello)</I>", 
"<P CLASS=center><I>(La foto si apre in un altro pannello)</I>", 
"<P CLASS=center><I>(Altrove su questa pagina)</I>", 
IClickHere+"la nota<BR>dell\' autore a piè di pagina.", 
IClickHere+"la mia nota a piè di pagina.", 
IClickHere+"tornare al riferimento nel testo.", 
"<P CLASS=center>Se questo non vi dice nulla, basta cliccare per la spiegazione.<BR><I>(La pagina si apre in un altro pannello)</I>", 
"<P CLASS=center><SPAN CLASS=alert>(HAC in fenestra aperietur pagina)</SPAN>", 
"<P CLASS=center><I>(Altera in fenestra aperietur pagina)</I>", 
"<P CLASS=center><I>(In alio situ: altera in fenestra aperietur pagina)</I>", 
"<P CLASS=center><I>(Altera in fenestra aperietur haec seu conexa photo)</I>", 
"<P CLASS=center><I>(Altera in fenestra aperietur photo)</I>", 
"<P CLASS=center><I>(Alibi in hac pagina)</I>", 
"<P CLASS=center>Cliccare hic<BR>ad auctoris sive editoris<BR>adnotationem legendam<BR>in ima pagina", 
"<P CLASS=center>Cliccare hic<BR>ad adnotationem meam<BR>in ima pagina legendam", 
"<P CLASS=center>Cliccare hic<BR>ad revertendum in textum", 
" ", 
SZero, 
"<P CLASS=center><I>(La página abre en una otra ventana)</I>", 
"<P CLASS=center><I>(Fuera del sitio: la página abre en una otra ventana)</I>", 
"<P CLASS=center><I>(Esta foto o una foto relacionada, abre en una otra ventana)</I>", 
"<P CLASS=center><I>(La foto abre en una otra ventana)</I>", 
"<P CLASS=center><I>(Otra parte en esta página)</I>", 
SClickHere+"la nota del autor en bajo de la página.", 
SClickHere+"mi nota en bajo de la página.", 
SClickHere+"volver a la referencia en el texto.", 
" ", 
EClickHere+"the article in Smith\'s Dictionary."+EThisWindow, 
FClickHere+"l\' article de Smith\'s Dictionary."+FThisWindow, 
IClickHere+"<BR>l\' articolo<BR>di Smith\'s Dictionary."+IThisWindow, 
" ", 
SClickHere+"el artículo de Smith\'s Dictionary.<BR><SPAN CLASS=alert>(Abre en ESTA ventana)</SPAN>", 
EClickHere+"the article in Smith\'s Dictionary.<BR><I>(Page opens in another window)</I>", 
FClickHere+"l\' article de Smith\'s Dictionary.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"l\' articolo di Smith\'s Dictionary.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
SClickHere+"el artículo de Smith\'s Dictionary.<BR><I>(Abre en una otra ventana)</I>", 
"<P CLASS=center>If you don\'t know what this is about,<BR>the explanation is only a click away."+EThisWindow, 
"<P CLASS=center>Si vous ne savez pas ce de quoi il s\'agit,<BR>il n\'y a qu\'à faire clic pour l\'explication."+FThisWindow, 
"<P CLASS=center>Se non sapete che cosa è,<BR>basta cliccare qui per la spiegazione."+IThisWindow, 
" ", 
" ", 
"<P CLASS=center>If you don\'t know what this is about,<BR>the explanation is only a click away.<BR><I>(Offsite: opens in another window)</I>", 
"<P CLASS=center>Si vous ne savez pas ce de quoi il s\'agit,<BR>il n\'y a qu\'à faire clic pour l\'explication.<BR><I>(Hors site: s\'ouvre dans une autre fenêtre)</I>", 
"<P CLASS=center>Se non sapete che cosa è,<BR>basta cliccare qui per la spiegazione.<BR><I>(Fuori sito: si apre in un altro pannello)</I>", 
" ", 
" ", 
EClickHere+"the relevant section<BR>of an article<BR>in Smith\'s Dictionary."+EThisWindow, 
FClickHere+"le passage ou le chapitre de l\' article<BR>de Smith\'s Dictionary."+FThisWindow, 
IClickHere+"la parte corrispettiva di un articolo<BR>di Smith\'s Dictionary."+IThisWindow, 
" ", 
SClickHere+"la parte relativa del artículo de Smith\'s Dictionary.<BR><SPAN CLASS=alert>(Abre en ESTA ventana)</SPAN>", 
EClickHere+"the relevant section<BR>of an article<BR>in Smith\'s Dictionary.<BR><I>(Page opens<BR>in another window)</I>", 
FClickHere+"le passage ou le chapitre de l\' article<BR>de Smith\'s Dictionary.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"la parte corrispettiva di un articolo<BR>di Smith\'s Dictionary.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
SClickHere+"la parte relativa del artículo de Smith\'s Dictionary.<BR><I>(Abre en una otra ventana)</I>", 
PZero, 
"<P CLASS=center><I>(A página abre em uma outra janela)</I>", 
"<P CLASS=center><I>(Offsite: a página abre em uma outra janela)</I>", 
"<P CLASS=center><I>(Esta foto ou uma foto relacionada, abre em uma outra janela)</I>", 
"<P CLASS=center><I>(A foto abre em uma outra janela)</I>", 
"<P CLASS=center><I>(Em outro lugar desta página)</I>", 
PClickHere+"a anotação do autor no fim da página.", 
PClickHere+"a minha anotação no fim da página.", 
PClickHere+"voltar para a referência no texto.", 
" ", 
EClickHere+"the main index page of Smith\'s Dictionary.<BR><I>(Opens in a separate index window)</I>", 
FClickHere+"la page principale de Smith\'s Dictionary.<BR><I>(S\'ouvre dans une autre fenêtre-index)</I>", 
IClickHere+"la pagina principale di Smith\'s Dictionary.<BR><I>(Si apre in un altro pannello-indice)</I>", 
" ", 
SClickHere+"la página principal de Smith\'s Dictionary.<BR><I>(Abre en una otra ventana-indice)</I>", 
" ", 
"<P CLASS=center>Click here<BR>for the text discussion.<BR><I>(Elsewhere on this page)</I>", 
EClickHere+"the main index page of Smith\'s Dictionary."+EThisWindow, 
EClickHere+"the main index page of Daremberg &amp; Saglio\'s Dictionary.<BR><I>(Opens in a separate index window)</I>", 
EClickHere+"the main index page of Daremberg &amp; Saglio\'s Dictionary."+EThisWindow, 
EClickHere+"the article in Platner\'s <I>Topographical Dictionary of Ancient Rome</I>.<BR><SPAN CLASS=alert>(Page opens in THIS window)</SPAN>", 
FClickHere+"l\'article dans le Topographical Dictionary of Ancient Rome de Platner.<BR><SPAN CLASS=alert>(La page s\'ouvre dans CETTE fenêtre)</SPAN>", 
IClickHere+"l\' articolo nel <I>Topographical Dictionary of Ancient Rome</I> del Platner."+IThisWindow, 
"<P CLASS=center>Cliccare hic ad articulum legendum <BR>in Platneri <I>Topographical Dictionary of Ancient Rome</I>.<BR><SPAN CLASS=alert>(Anglice, HANC in fenestram aperietur pagina)</SPAN>", 
SClickHere+"el artículo en el Topographical Dictionary of Ancient Rome de Platner.<BR><SPAN CLASS=alert>(Abre en ESTA ventana)</SPAN>", 
EClickHere+"the article in Platner\'s Topographical Dictionary of Ancient Rome.<BR><I>(Page opens in another window)</I>", 
FClickHere+"l\'article dans le Topographical Dictionary of Ancient Rome de Platner.<BR><I>(La page s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"l\' articolo nel Topographical Dictionary of Ancient Rome del Platner.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
"<P CLASS=center>Cliccare hic ad articulum legendum <BR>in Platneri Topographical Dictionary of Ancient Rome.<BR><I>(Anglice, altera in fenestra aperietur pagina)", 
SClickHere+"el artículo en el Topographical Dictionary of Ancient Rome de Platner.<BR><I>(Abre en una otra ventana)</I>", 
EClickHere+"the article in Platner\'s Topographical Dictionary of Ancient Rome, with one or more photos.<BR><SPAN CLASS=alert>(Page opens in THIS window)</SPAN>", 
FClickHere+"l\'article dans le Topographical Dictionary of Ancient Rome de Platner, avec une ou plusieurs photos.<BR><SPAN CLASS=alert>(La page s\'ouvre dans CETTE fenêtre)</SPAN>", 
IClickHere+"l\' articolo nel Topographical Dictionary of Ancient Rome del Platner, con una o parecchie foto."+IThisWindow, 
"<P CLASS=center>Cliccare hic ad articulum legendum <BR>in Platneri <I>Topographical Dictionary of Ancient Rome</I>,<BR>una pluribusve cum photographiis.<BR><SPAN CLASS=alert>(Anglice, HANC in fenestram aperietur pagina)</SPAN>", 
" ", 
EClickHere+"the article in Platner\'s Topographical Dictionary of Ancient Rome, with one or more photos.<BR><I>(Page opens in another window)</I>", 
FClickHere+"l\'article dans le Topographical Dictionary of Ancient Rome de Platner, avec une ou plusieurs photos.<BR><I>(La page s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"l\' articolo nel Topographical Dictionary of Ancient Rome del Platner, con una o parecchie foto.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
"<P CLASS=center>Cliccare hic ad articulum legendum <BR>in Platneri Topographical Dictionary of Ancient Rome,<BR>una plurisve photographiis.<BR><I>(Anglice, altera in fenestra aperietur pagina)", 
" ", 
EClickHere+"the relevant section of an article in Platner\'s Topographical Dictionary of Ancient Rome.<BR><SPAN CLASS=alert>(Page opens in THIS window)</SPAN>", 
FClickHere+"la partie relative à ce sujet dans l\'article du <I>Topographical Dictionary of Ancient Rome</I> de Platner.<BR><SPAN CLASS=alert>(La page s\'ouvre dans CETTE fenêtre)</SPAN>", 
IClickHere+"la parte pertinente di un articolo nel Topographical Dictionary of Ancient Rome del Platner."+IThisWindow, 
" ", 
SClickHere+"la parte pertinente de un artículo en el Topographical Dictionary of Ancient Rome de Platner.<BR><SPAN CLASS=alert>(Abre en ESTA ventana)</SPAN>", 
EClickHere+"the relevant section of an article in Platner\'s <I>Topographical Dictionary of Ancient Rome</I>.<BR><I>(Page opens in another window)</I>", 
FClickHere+"la partie relative à ce sujet dans l\'article du Topographical Dictionary of Ancient Rome de Platner.<BR><I>(La page s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"la parte pertinente di un articolo nel Topographical Dictionary of Ancient Rome del Platner.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
SClickHere+"la parte pertinente de un  artículo en el Topographical Dictionary of Ancient Rome de Platner.<BR><I>(Abre en una otra ventana)</I>", 
EClickHere+"the complete work(s), onsite.<BR><SPAN CLASS=alert>(Page opens in THIS window)</SPAN>", 
" ", 
" ", 
" ", 
" ", 
EClickHere+"the complete work(s), onsite.<BR><I>(Page opens in another window)</I>", 
" ", 
" ", 
" ", 
" ", 
EClickHere+"Armellini\'s<BR><I>Chiese di Roma</I>,<BR>to this passage.<BR><I>(In Italian;<BR><SPAN CLASS=alert>page opens in THIS window</SPAN>)</I>", 
FClickHere+"<I>Chiese di Roma</I> de Mariano Armellini, à ce passage.<BR><SPAN CLASS=alert>(en italien; la page s\'ouvre dans CETTE fenêtre)</SPAN>", 
IClickHere+"le <I>Chiese di Roma</I> dell\' Armellini, a questo passo."+IThisWindow, 
" ", 
" ", 
EClickHere+"Armellini\'s<BR><I>Chiese di Roma</I>,<BR>to this passage.<BR><I>(In Italian;<BR>page opens<BR>in another window)</I>", 
FClickHere+"<I>Chiese di Roma</I> de Mariano Armellini, à ce passage.<BR><I>(en italien; la page s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"le <I>Chiese di Roma</I> dell\' Armellini, a questo passo.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
" ", 
EClickHere+"Christian Hülsen\'s<BR><I>Chiese di Roma nel Medio Evo</I>,<BR>to this passage or section.<BR>(<I>In Italian;</I><BR><SPAN CLASS=alert>page opens in THIS window)</SPAN>", 
FClickHere+"<I>Chiese di Roma nel Medio Evo</I> de Christian Hülsen, à ce passage.<BR><I>(en italien; <SPAN CLASS=alert>la page s\'ouvre dans CETTE fenêtre</SPAN>)</I>", 
IClickHere+"le <I>Chiese di Roma nel Medio Evo</I> di Christian Hülsen, a questo passo."+IThisWindow, 
" ", 
" ", 
EClickHere+"Christian Hülsen\'s<BR><I>Chiese di Roma nel Medio Evo</I>,<BR>to this passage or section.<BR><I>(In Italian;<BR>page opens in another window)</I>", 
FClickHere+"<I>Chiese di Roma nel Medio Evo</I> de Christian Hülsen, à ce passage.<BR><I>(en italien; la page s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"le <I>Chiese di Roma nel Medio Evo</I> di Christian Hülsen, a questo passo.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
" ", 
EClickHere+"my homepage for this church,<BR>with the texts of Armellini, Hülsen, and Titi,<BR>plus photos and offsite links.<BR><SPAN CLASS=alert>(Page opens in THIS window)</SPAN>", 
FClickHere+"mon site sur cette église,<BR>avec les textes d\'Armellini, de Hülsen, et de Titi,<BR>ainsi que des photos et des liens hors site."+FThisWindow, 
IClickHere+"il mio sito sulla chiesa,<BR>con i testi dell\' Armellini, del Hülsen, e/o del Titi;<BR>e con fotografie e links fuori sito."+IThisWindow, 
" ", 
SClickHere+"mi sitio sobre esta iglesia, con los textos de Armellini, de Hülsen, y de Titi; y con fotos y enlaces externos.<BR><SPAN CLASS=alert>(Abre en ESTA ventana)</SPAN>", 
EClickHere+"my homepage for this church, with the texts of Armellini, Hülsen, and Titi, plus photos and offsite links.<BR><I>(Page opens in another window)</I>", 
FClickHere+"mon site sur cette église, avec les textes d\'Armellini, de Hülsen, et de Titi, ainsi que des photos et des liens hors site.<BR><I>(S\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il mio sito sulla chiesa, con i testi dell\' Armellini, del Hülsen, e/o del Titi; e con fotografie e links fuori sito.<BR><I>(Si apre in un altro pannello)</I>", 
" ", 
SClickHere+"mi sitio sobre esta iglesia, con los textos de Armellini, de Hülsen, y de Titi; y con fotos y enlaces externos.<BR><I>(Abre en una otra ventana)</I>", 
EClickHere+"the article in Daremberg &amp; Saglio\'s Dictionary.<BR><SPAN CLASS=alert>(Page opens in THIS window)</SPAN>", 
FClickHere+"l\' article du Dictionnaire de Daremberg &amp; Saglio."+FThisWindow, 
IClickHere+"l\' articolo del Dizionario di Daremberg e Saglio."+IThisWindow, 
" ", 
SClickHere+"el artículo del Diccionario de Daremberg y Saglio.<BR><SPAN CLASS=alert>(Abre en ESTA ventana)</SPAN>", 
EClickHere+"the article in Daremberg &amp; Saglio\'s Dictionary.<BR><I>(Page opens in another window)</I>", 
FClickHere+"l\' article du Dictionnaire de Daremberg &amp; Saglio.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"l\' articolo del Dizionario di Daremberg e Saglio.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
SClickHere+"el artículo del Diccionario de Daremberg y Saglio.<BR><I>(Abre en una otra ventana)</I>", 
EClickHere+"my page."+EThisWindow, 
FClickHere+"ma page."+FThisWindow, 
IClickHere+"la mia pagina."+IThisWindow, 
" ", 
SClickHere+"mi página.<BR><SPAN CLASS=alert>(Abre en ESTA ventana)</SPAN>", 
EClickHere+"my page.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"ma page.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"la mia pagina.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
SClickHere+"mi página.<BR><I>(Abre en una otra ventana)</I>", 
EClickHere+"my pages.<BR><I>(Orientation page opens in THIS window)</I>", 
FClickHere+"mes pages.<BR><I>(La page d\'orientation s\'ouvre dans CETTE fenêtre)</I>", 
IClickHere+"le mie pagine.<BR><I>(La pagina di orientazione si apre in QUESTO pannello)</I>", 
" ", 
SClickHere+"mis páginas.<BR><I>(La página de orientación abre en ESTA ventana)</I>", 
EClickHere+"my pages.<BR><I>(Orientation page opens in another window)</I>", 
FClickHere+"mes pages.<BR><I>(La page d\'orientation s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"le mie pagine.<BR><I>(La pagina di orientazione si apre in un altro pannello)</I>", 
" ", 
SClickHere+"mis páginas.<BR><I>(La página de orientación abre en una otra ventana)</I>", 
EClickHere+"my page on this church, with photos."+EThisWindow, 
FClickHere+"ma page sur cette église, avec photos."+FThisWindow, 
IClickHere+"la mia pagina su questa chiesa, con delle foto."+IThisWindow, 
" ", 
SClickHere+"mi página sobre esta iglesia, con fotos.<BR><SPAN CLASS=alert>(Abre en ESTA ventana)</SPAN>", 
EClickHere+"my page on this church, with photos.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"ma page sur cette église, avec photos.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"la mia pagina su questa chiesa, con delle foto.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
SClickHere+"mi página sobre esta iglesia, con fotos.<BR><I>(Abre en una otra ventana)</I>", 
EClickHere+"my pages on this church, with photos.<BR><I>(Orientation page<BR>opens in THIS window)</I>", 
FClickHere+"mes pages sur cette église, avec photos.<BR><I>(La page d\'orientation s\'ouvre dans CETTE fenêtre)</I>", 
IClickHere+"le mie pagine su questa chiesa, con delle foto.<BR><I>(La pagina di orientazione si apre in QUESTO pannello)</I>", 
" ", 
SClickHere+"mis páginas sobre esta iglesia, con fotos.<BR><I>(La página de orientación abre en ESTA ventana)</I>", 
EClickHere+"my pages on this church, with photos.<BR><I>(Orientation page<BR>opens in another window)</I>", 
FClickHere+"mes pages sur cette église, avec photos.<BR><I>(La page d\'orientation s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"le mie pagine su questa chiesa, con delle foto.<BR><I>(La pagina di orientazione si apre in un altro pannello)</I>", 
" ", 
SClickHere+"mis páginas sobre esta iglesia, con fotos.<BR><I>(La página de orientación abre en una otra ventana)</I>", 
EClickHere+"my site on this town,<BR>with photos and links.<BR><I>(Orientation page opens in THIS window)</I>", 
FClickHere+"mes pages sur cette ville,<BR>avec photos et liens.<BR><I>(La page d\'orientation s\'ouvre dans CETTE fenêtre)</I>", 
IClickHere+"le mie pagine su questa città,<BR>con fotografie e un elenco di link.<BR><I>(La pagina di orientazione si apre in QUESTO pannello)</I>", 
" ", 
SClickHere+"mis páginas sobre esta ciudad,<BR>con fotos y enlaces.<BR><I>(La página de orientación abre en ESTA ventana)</I>", 
EClickHere+"my site on this town,<BR>with photos and links.<BR><I>(Orientation page opens in another window)</I>", 
FClickHere+"mes pages sur cette ville,<BR>avec photos et liens.<BR><I>(La page d\'orientation s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"le mie pagine su questa città,<BR>con fotografie e un elenco di link.<BR><I>(La pagina di orientazione si apre in un altro pannello)</I>", 
" ", 
SClickHere+"mis páginas sobre esta ciudad,<BR>con fotos y enlaces.<BR><I>(La página de orientación abre en una otra ventana)</I>", 
EClickHere+"the passage<BR>in an English translation<BR>linked to the original <SPAN CLASS=Latin>Latin</SPAN>.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I></CENTER>",  //"THIS IS WHAT REALLY BELONGS IN 520:<CENTER>Click here for the passage<BR>in the <SPAN CLASS=Latin>Latin</SPAN> text of Suetonius,<BR>linked to an English translation. <BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"le passage<BR>en traduction anglaise<BR>lié au texte <SPAN CLASS=Latin>latin</SPAN>.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"il passo<BR>in una traduzione inglese<BR>collegato al testo latino.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN></CENTER>", //"THIS IS WHAT REALLY BELONGS IN 522:<CENTER>Cliccare qui per il passo<BR>nel testo latino di Svetonio,<BR>collegato a traduzioni in inglese e francese.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
"<P CLASS=center>Cliccare hic ad legendum<BR>in anglica versione<BR>ad Latinum textum conexum.<BR><I>(Altera in fenestra aperietur pagina)</I>", 
SClickHere+"este pasaje<BR>en una traducción inglesa<BR>con enlace al texto latino.<BR><I>(Abre en una otra ventana)</I>", 
EClickHere+"the passage<BR>in an English translation<BR>linked to the original <SPAN CLASS=Latin>Latin</SPAN>.<BR><I>(Offsite, opens in another window)</I></CENTER>",  //"THIS IS WHAT REALLY BELONGS IN 525:<CENTER>Click here for the passage<BR>in the <SPAN CLASS=Latin>Latin</SPAN> text of Suetonius,<BR>linked to an English translation. <BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"le passage<BR>en traduction anglaise<BR>lié au texte <SPAN CLASS=Latin>latin</SPAN>.<BR><I>(Hors site, s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il passo<BR>in una traduzione inglese<BR>collegato al testo latino.<BR><I>(Fuori sito, si apre in un altro pannello)</I></CENTER>", //"THIS IS WHAT REALLY BELONGS IN 507:<CENTER>Cliccare qui per il passo<BR>nel testo latino di Svetonio,<BR>collegato a traduzioni in inglese e francese.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
"<P CLASS=center>Cliccare hic ad legendum<BR>in anglica versione<BR>ad Latinum textum conexum.<BR><I>(Apud alios, altera in fenestra aperietur pagina)</I>", 
SClickHere+"este pasaje<BR>en una traducción inglesa<BR>con enlace al texto latino.<BR><I>(Fuera del sitio, abre en una otra ventana)</I>", 
EClickHere+"the passage<BR>in the original <SPAN CLASS=Latin>Latin</SPAN><BR>linked to an English translation.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I></CENTER>",  //"THIS IS WHAT REALLY BELONGS IN 510:<CENTER>Click here for the passage<BR>in the <SPAN CLASS=Latin>Latin</SPAN> text of Suetonius,<BR>linked to an English translation. <BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"le passage<BR>dans le texte <SPAN CLASS=Latin>latin</SPAN><BR>lié à une traduction anglaise.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"il passo<BR>nel testo latino<BR>collegato ad una traduzione inglese.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN></CENTER>", //"THIS IS WHAT REALLY BELONGS IN 512:<CENTER>Cliccare qui per il passo<BR>nel testo latino di Svetonio,<BR>collegato a traduzioni in inglese e francese.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
"<P CLASS=center>Cliccare hic ad legendum<BR>Latinum textum<BR>ad anglicam versionem conexum.<BR><I>(Altera in fenestra aperietur pagina)</I>", 
SClickHere+"este pasaje<BR>en el texto latino<BR>con enlace a una traducción inglesa.<BR><I>(Abre en una otra ventana)</I>", 
EClickHere+"the passage<BR>in the original <SPAN CLASS=Latin>Latin</SPAN><BR>linked to an English translation.<BR><I>(Offsite, opens in another window)</I></CENTER>",  //"THIS IS WHAT REALLY BELONGS IN 515:<CENTER>Click here for the passage<BR>in the <SPAN CLASS=Latin>Latin</SPAN> text of Suetonius,<BR>linked to an English translation. <BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"le passage<BR>dans le texte <SPAN CLASS=Latin>latin</SPAN><BR>lié à une traduction anglaise.<BR><I>(Hors site, s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il passo<BR>nel testo latino<BR>collegato ad una traduzione inglese.<BR><I>(Fuori sito, si apre in un altro pannello)</I></CENTER>", //"THIS IS WHAT REALLY BELONGS IN 517:<CENTER>Cliccare qui per il passo<BR>nel testo latino di Svetonio,<BR>collegato a traduzioni in inglese e francese.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
"<P CLASS=center>Cliccare hic ad legendum<BR>Latinum textum<BR>ad anglicam versionem conexum.<BR><I>(Apud alios, altera in fenestra aperietur pagina)</I>", 
SClickHere+"este pasaje<BR>en el texto latino<BR>con enlace a una traducción inglesa.<BR><I>(Fuera del sitio, abre en una otra ventana)</I>", 
EClickHere+"the passage<BR>in Pliny the Elder\'s Natural History.<BR><I>(<SPAN CLASS=Latin>Latin</SPAN>, opens in another window)</I>", 
FClickHere+"le passage<BR>dans l\'Histoire Naturelle de Pline l\'ancien.<BR><I>(En <SPAN CLASS=Latin>latin</SPAN>; s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il passo<BR>nella Storia Naturale di Plinio il Vecchio.<BR><I>(In latino; si apre in un altro pannello)</I>", 
" ", 
SClickHere+"el pasaje<BR>en la Historia Natural de Plinio el Viejo.<BR><I>(En latín; abre en una otra ventana)</I>", 
EClickHere+"the passage<BR>in Ptolemy\'s Geography.<BR><I>(English, opens in another window)</I>", 
FClickHere+"le passage<BR>dans la Géographie de Ptolémé.<BR><I>(En anglais; s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il passo<BR>nella Geografia di Tolomeo.<BR><I>(In inglese; si apre in un altro pannello)</I>", 
"<P CLASS=center>Cliccare hic ad textum legendum <BR>in Geographia Ptolemaei.<BR><I>(Anglice, altera in fenestra aperietur pagina)", 
" ", 
EClickHere+"the passage<BR>in Ammian<BR>in an English translation<BR>linked to the original <SPAN CLASS=Latin>Latin</SPAN>.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"le passage<BR>dans Ammien<BR>en traduction anglaise<BR>liée au texte <SPAN CLASS=Latin>latin</SPAN>.<SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
"<CENTER>Cliccare qui per il passo<BR>in Ammiano<BR>in una traduzione inglese<BR>collegato al testo latino.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
" ", 
EClickHere+"the passage<BR>in Appian.<BR><I>(English, opens in another window)</I>", 
FClickHere+"le passage<BR>dans Appien.<BR><I>(En anglais; s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il passo<BR>in Appiano.<BR><I>(In inglese; si apre in un altro pannello)</I>", 
" ", 
" ", 
EClickHere+"the passage<BR>in Cassius Dio\'s History.<BR><I>(English, opens in another window)</I>", 
FClickHere+"le passage<BR>dans l\'Histoire de Dion Cassius.<BR><I>(En anglais; s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il passo<BR>nella Storia di Cassio Dione.<BR><I>(In inglese; si apre in un altro pannello)</I>", 
" ", 
SClickHere+"el pasaje<BR>en Dion Cásio.<BR><I>(en inglés, abre en una otra ventana)</I>", 
EClickHere+"the passage<BR>in Plutarch.<BR><I>(English, opens in another window)</I>", 
FClickHere+"le passage<BR>dans Plutarque.<BR><I>(En anglais; s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il passo<BR>in Plutarco.<BR><I>(In inglese; si apre in un altro pannello)</I>", 
" ", 
SClickHere+"el pasaje<BR>en Plutarco.<BR><I>(en inglés, abre en una otra ventana)</I>", 
EClickHere+"the passage<BR>in Polybius\' Histories.<BR><I>(English, opens in another window)</I>", 
FClickHere+"le passage<BR>dans les Histoires de Polybe.<BR><I>(En anglais; s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il passo<BR>nelle Storie di Polibio.<BR><I>(In inglese; si apre in un altro pannello)</I>", 
"<P CLASS=center>Cliccare hic ad textum legendum <BR>in Historiis Polybii.<BR><I>(Anglice, altera in fenestra aperietur pagina)", 
" ", 
EClickHere+"the passage<BR>in Strabo\'s Geography.<BR><I>(English, opens in another window)</I>", 
FClickHere+"le passage<BR>dans la Géographie de Strabon.<BR><I>(En anglais; s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il passo<BR>nella Geografia di Strabone.<BR><I>(In inglese; si apre in un altro pannello)</I>", 
"<P CLASS=center>Cliccare hic ad textum legendum <BR>in Geographia Strabonis.<BR><I>(Anglice, altera in fenestra aperietur pagina)", 
" ", 
IClickHere+"la scheda di questa chiesa.<BR><I>(Rimane in questo pannello)</I>", 
IClickHere+"la scheda di questa chiesa.<BR><I>(Un\' altra pagina si apre in QUESTO pannello)</I>", 
IClickHere+"la scheda di quest\' artista nell\'  indice."+IThisWindow, 
IClickHere+"la scheda di quest\' artista nell\'  indice.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
IClickHere+"il catalogo,<BR>al passo preciso.<BR><I>(Si aprirà nel pannello dei cataloghi)</I>", 
IClickHere+"questo quadro della pianta.<BR><I>(Si aprirà nel pannello delle piante)</I>", 
IClickHere+"QUESTO QUADRO ADIACENTE.<BR><I>(Rimane in questo pannello)</I>", 
IClickHere+"questa chiesa.<BR><I>(Si apre nel pannello principale del testo)</I>", 
EClickHere+"this artist\'s entry in the index.<BR><I>(Open in THIS window)</I>", 
EClickHere+"this artist\'s entry in the index.<BR><I>(Open in another window)</I>", 
EClickHere+"my site or page."+EThisWindow, 
FClickHere+"mon site ou ma page."+FThisWindow, 
IClickHere+"il mio sito o la mia pagina."+IThisWindow, 
" ", 
SClickHere+"mi sitio o página.<BR><SPAN CLASS=alert>(Abre en ESTA ventana)</SPAN>", 
EClickHere+"my site or page.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"mon site ou ma page.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"il mio sito o la mia pagina.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
SClickHere+"mi sitio o página.<BR><I>(Abre en una otra ventana)</I>", 
EClickHere+"my subsite,<BR>with several pages, photos, etc."+EThisWindow, 
FClickHere+"mon sous-site,<BR>qui comporte plusieurs pages, photos, etc."+FThisWindow, 
IClickHere+"il mio sotto-sito,<BR>con parecchie pagine e immagini, ecc."+IThisWindow, 
" ", 
SClickHere+"mi sub-sitio,<BR>con varias páginas, imágenes, etc.<BR><SPAN CLASS=alert>(Abre en ESTA ventana)</SPAN>", 
EClickHere+"my subsite,<BR>with several pages, photos, etc.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"mon sous-site,<BR>qui comporte plusieurs pages, photos, etc.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"il mio sotto-sito,<BR>con parecchie pagine e immagini, ecc.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
SClickHere+"mi sub-sitio,<BR>con varias páginas, imágenes, etc.<BR><I>(Abre en una otra ventana)</I>", 
EClickHere+"my subsite,<BR>with many pages, photos, links."+EThisWindow, 
FClickHere+"mon sous-site,<BR>qui comporte de nombreux pages, photos, et liens."+FThisWindow, 
IClickHere+"il mio sotto-sito,<BR>con molti pagine, immagini, link."+IThisWindow, 
" ", 
SClickHere+"mi sub-sitio,<BR>con muchas páginas, imágenes, y enlaces.<BR><SPAN CLASS=alert>(Abre en ESTA ventana)</SPAN>", 
EClickHere+"my subsite,<BR>with many pages, photos, links.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"mon sous-site,<BR>qui comporte de nombreuses pages et photos, et de nombreux liens.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"il mio sotto-sito,<BR>con molte pagine e immagini, e molti link.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
SClickHere+"mi sub-sitio,<BR>con muchas páginas y imagenes, y muchos enlaces.<BR><I>(Abre en una otra ventana)</I>", 
"<P CLASS=center>The entire book is onsite.<BR><I>(Orientation page opens in THIS window)</I>", 
"<P CLASS=center>Le livre entier se trouve sur le site.<BR><I>(La page d\'orientation s\'ouvre dans CETTE fenêtre)</I>", 
"<P CLASS=center>Il libro intero si trova sul sito.<BR><I>(La pagina di orientazione si apre in QUESTO pannello)</I>", 
" ", 
"<P CLASS=center>El libro entero es reproducido en este sitio.<BR><I>(La página de orientación abre en ESTA ventana)</I>", 
"<P CLASS=center>The entire book is onsite.<BR><I>(Orientation page opens in another window)</I>", 
"<P CLASS=center>Le livre entier se trouve sur le site.<BR><I>(La page d\'orientation s\'ouvre dans une autre fenêtre)</I>", 
"<P CLASS=center>Il libro intero si trova sul sito.<BR><I>(La pagina di orientazione si apre in un altro pannello)</I>", 
" ", 
"<P CLASS=center>El libro entero es reproducido en este sitio.<BR><I>(La página de orientación abre en una otra ventana)</I>", 
EClickHere+"their website or page.<BR><I>(Offsite, so it opens in another window)</I>", 
FClickHere+"leur site ou page.<BR><I>(Hors site, s\'ouvrira donc dans une autre fenêtre)</I>", 
IClickHere+"loro sito o pagina.<BR><I>(Fuori sito, si apre quindi in un altro pannello)</I>", 
" ", 
SClickHere+"su sitio o página.<BR><I>(Sitio externo: abre en una otra ventana)</I>", 
" ", 
" ", 
" ", 
" ", 
" ", 
EClickHere+"the original <SPAN CLASS=Latin>Latin</SPAN>.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"le <SPAN CLASS=Latin>latin</SPAN> original.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"il latino originale.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
SClickHere+"el latino originale.<BR><I>(Abre en una otra ventana)</I>", 
" ", 
" ", 
" ", 
" ", 
" ", 
EClickHere+"the passage<BR>in the <SPAN CLASS=Latin>Latin</SPAN> text.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"le passage du texte <SPAN CLASS=Latin>latin</SPAN>.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"il passo dell\' autore latino.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
SClickHere+"el pasaje del autor latino.<BR><I>(Abre en una otra ventana)</I>", 
EClickHere+"the passage<BR>in a <SPAN CLASS=Latin>Latin</SPAN> translation.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"le passage dans une traduction latine.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"il passo del testo tradotto in latino.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
SClickHere+"el pasaje del autor latino.<BR><I>(Abre en una otra ventana)</I>", 
EClickHere+"the passage<BR>in the <SPAN CLASS=Latin>Latin</SPAN> text.<BR><I>(Offsite: opens in another window)</I>", 
FClickHere+"le passage du texte <SPAN CLASS=Latin>latin</SPAN>.<BR><I>(Hors site: s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il passo del testo latino.<BR><I>(Fuori sito: si apre in un altro pannello)</I>", 
" ", 
SClickHere+"el pasaje del texto latino.<BR><I>(Fuera del sitio: abre en una otra ventana)</I>", 
EClickHere+"the passage<BR>in the <SPAN CLASS=Latin>Latin</SPAN> text,<BR>linked to a translation<BR><I>(Offsite: opens in another window)</I>", 
FClickHere+"le passage du texte <SPAN CLASS=Latin>latin</SPAN>.<BR>liée à une traduction<I>(Hors site: s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il passo del testo latino.<BR>collegato ad una traduzione<BR><I>(Fuori sito: si apre in un altro pannello)</I>", 
" ", 
SClickHere+"el pasaje del texto latino.<BR>con enlace a una traducción<I>(Fuera del sitio: abre en una otra ventana)</I>", 
EClickHere+"the passage<BR>in the <SPAN CLASS=Latin>Latin</SPAN> text,<BR>linked to one or more translations.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"le passage du texte <SPAN CLASS=Latin>latin</SPAN>,<BR>lié à une ou plusieurs traductions.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"il passo dell\' autore latino,<BR>collegato ad una o più traduzioni.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
SClickHere+"el pasaje del autor latino,<BR>con enlace a una o mas traducciones.<BR><I>(Abre en una otra ventana)</I>", 
EClickHere+"the passage in the <SPAN CLASS=Latin>Latin</SPAN> text,<BR>linked to one or more translations.<BR><I>(Offsite: opens in another window)</I>", 
FClickHere+"le passage du texte <SPAN CLASS=Latin>latin</SPAN>,<BR>lié à une ou plusieurs traductions.<BR><I>(Hors site: s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il passo dell\' autore latino,<BR>collegato ad una o più traduzioni.<BR><I>(Fuori sito: si apre in un altro pannello)</I>", 
" ", 
SClickHere+"el pasaje del autor latino,<BR>con enlace a una o mas traducciones.<BR><I>(Fuera del sitio: abre en una otra ventana)</I>", 
EClickHere+"the text of this passage<BR>in the original language.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"le texte de ce passage<BR>dans la langue originale.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"il testo di questo passo<BR>nella lingua originaria.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
"<P CLASS=center>Cliccare hic ad legendum textum<BR>in lingua originali.<BR><I>(Altera in fenestra aperietur pagina)</I>", 
SClickHere+"el texto de este pasaje<BR>en la lingua original.<BR><I>(Abre en una otra ventana)</I>", 
EClickHere+"the text of this passage<BR>in the original language.<BR><I>(Offsite: opens in another window)</I>", 
FClickHere+"le texte de ce passage<BR>dans la langue originale.<BR><I>(Hors site: s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il testo di questo passo<BR>nella lingua originaria.<BR><I>(Fuori sito: si apre in un altro pannello)</I>", 
"<P CLASS=center>Cliccare hic ad legendum textum<BR>in lingua originali.<BR><I>(In situ externo: altera in fenestra aperietur pagina)</I>", 
SClickHere+"el texto de este pasaje<BR>en la lingua original.<BR><I>(Fuera del sitio: abre en una otra ventana)</I>", 
EClickHere+"an English translation<BR>of this passage.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"une traduction en français de ce passage.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"una traduzione italiana di questo passo.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
SClickHere+"una traducción en castellano de este parágrafo.<BR><I>(Abre en una otra ventana)</I>", 
EClickHere+"an English translation.<BR><I>(Offsite: opens in another window)</I>", 
FClickHere+"une traduction en français.<BR><I>(Hors site: s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"una traduzione italiana.<BR><I>(Fuori sito: si apre in un altro pannello)</I>", 
" ", 
SClickHere+"una traducción en castellano.<BR><I>(Fuera del sitio: abre en una otra ventana)</I>", 
CZero, 
"<P CLASS=center><I>(La pàgina s\'obre en una altra finestra)</I>", 
"<P CLASS=center><I>(Fora d\'aquest lloc: la pàgina s\'obre en una altra finestra)</I>", 
"<P CLASS=center><I>(Aquesta foto o una foto relacionada, s\'obre en una altra finestra)</I>", 
"<P CLASS=center><I>(La foto s\'obre en una altra finestra)</I>", 
"<P CLASS=center><I>(En una altra part d\'aquesta pàgina)</I>", 
CClickHere+"la nota de l'autor a peu de la pàgina.", 
CClickHere+"la meva nota a peu de la pàgina.", 
CClickHere+"torna a la referència en el text.", 
" ", 
"<P CLASS=center><I>(Offsite page<BR>opens in another window)</I><BR><FONT COLOR=FF0000><B>Warning: PDF file.</B></SPAN>", 
" ", 
"<P CLASS=center><I>(La pagina, fuori sito,<BR>si apre in un altro pannello)</I><BR><FONT COLOR=FF0000><B>Attenzione: documento PDF.</B></SPAN>", 
" ", 
" ", 
"<P CLASS=center><I>(Page opens in another window)</I><BR><FONT COLOR=FF0000><B>JSTOR (limited access)</B></SPAN>", 
" ", 
" ", 
" ", 
" ", 
"<P CLASS=center><I>(Page opens in another window)</I><BR><FONT COLOR=FF0000><B>Warning: The page contains coding errors and may not be visible in all browsers.</B></SPAN>", 
" ", 
"<P CLASS=center><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN><BR><FONT COLOR=FF0000><B>Avvertimento: La pagina contiene errori di codaggio e può darsi che non sia visibile in tutti i navigatori.</B></SPAN>", 
" ", 
" ", 
"<P CLASS=center><I>(Page opens in another window)</I><BR><FONT COLOR=FF0000><B>Warning: loud soundfile; you may want to turn down your volume level before going there.</B></SPAN>", 
" ", 
" ", 
" ", 
" ", 
EClickHere+"the solution!<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"la solution!<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"la soluzione!<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
EClickHere+"the passage<BR>in Diodorus\' <I>Library of History</I>.<BR><I>(English, opens in another window)</I>", 
FClickHere+"le passage<BR>dans l\'Histoire de Diodore.<BR><I>(En anglais; s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il passo<BR>nella Storia di Diodoro.<BR><I>(In inglese; si apre in un altro pannello)</I>", 
"<P CLASS=center>Cliccare hic ad textum legendum <BR>in Historia Diodori.<BR><I>(Anglice, altera in fenestra aperietur pagina)", 
" ", 
EClickHere+"the passage of Herodotus<BR><I>(English, linked to the Greek original: opens in another window)</I>", 
FClickHere+"le passage d\'Hérodote<BR><I>(En anglais, lié à l'original grec : s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il passo di Erodoto<BR><I>(In inglese, collegato all' originale greco; si apre in un altro pannello)</I>", 
" ", 
" ", 
EClickHere+"the passage of Pausanias<BR><I>(Offsite: opens in another window)</I>", 
FClickHere+"le passage de Pausanias<BR><I>(Hors site: s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il passo di Pausania<BR><I>(Fuori sito: si apre in un altro pannello)</I>", 
" ", 
" ", 
EClickHere+"the passage of Thucydides<BR><I>(Offsite: opens in another window)</I>", 
FClickHere+"le passage de Thucydide<BR><I>(Hors site: s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il passo di Tucidide<BR><I>(Fuori sito: si apre in un altro pannello)</I>", 
" ", 
" ", 
EClickHere+"the passage<BR>in the <SPAN CLASS=Latin>Latin</SPAN> text of Frontinus,<BR>linked to an English translation.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"le passage<BR>dans le texte <SPAN CLASS=Latin>latin</SPAN> de Frontin,<BR>lié à une traduction anglaise.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"il passo<BR>nel testo latino di Frontino,<BR>collegato ad una traduzione in inglese.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
EClickHere+"the passage<BR>in an English translation of Frontinus,<BR>linked to the <SPAN CLASS=Latin>Latin</SPAN> text. <BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"le passage<BR>dans une traduction anglaise de Frontin,<BR>lié au texte <SPAN CLASS=Latin>latin</SPAN>. <BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
" ", 
" ", 
" ", 
EClickHere+"the passage<BR>in Dionysius in English translation<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
" ", 
IClickHere+"il passo<BR>di Dionisio in traduzione inglese<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
" ", 
"<P CLASS=center>If you don\'t know what this is about,<BR>the explanation is only a click away."+EThisWindow, 
"<P CLASS=center>Si vous ne savez pas ce de quoi il s\'agit,<BR>il n\'y a qu\'à faire clic pour l\'explication."+FThisWindow, 
"<P CLASS=center>Se questo non vi dice nulla,<BR>basta cliccare per la spiegazione.<BR><I>(La pagina si apre in QUESTO pannello)</I>", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
EClickHere+"the <SPAN CLASS=Latin>Latin</SPAN> original<BR>of this passage.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"l\'original <SPAN CLASS=Latin>latin</SPAN><BR>de ce passage.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"l\' originale latino<BR>di questo passo.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
" ", 
EClickHere+"the Greek original<BR>of this passage.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"l\'original grec<BR>de ce passage.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"l\' originale greco<BR>di questo passo.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
" ", 
"<P CLASS=center>This site comprises roughly 15,000 pages of text and photos, mostly about American history, ancient Rome, classical Antiquity, and central Italy.<BR><B><FONT COLOR=009900>CLICK ON THE LINK FOR THE HOMEPAGE.</SPAN></B><BR><SPAN CLASS=alert>(Opens in THIS window.)</SPAN>", 
"<P CLASS=center>Ce site comporte environ 15.000 pages de texte et de photos, surtout sur Rome antique et médiévale et l\'Italie centrale.<BR><B><FONT COLOR=009900>FAIRE CLIC SUR LE LIEN POUR LA PAGE D\'ACCUEIL.</SPAN></B><BR><SPAN CLASS=alert>(S\'ouvre dans CETTE fenêtre.)</SPAN>", 
"<P CLASS=center>Questo sito contiene circa 15.000 pagine di testo e di foto, innanzitutto sulla Roma antica e medioevale e l\'Italia centrale.<BR><B><FONT COLOR=009900>CLICCARE SUL LINK PER LA PAGINA HOME.</SPAN></B><BR><SPAN CLASS=alert>(Si apre in QUESTO pannello.)</SPAN>", 
"<P CLASS=center>Hic situs milia paginarum<BR>textus photographiarumque<BR>continet, plerumque<BR>de historia Americana,<BR>Roma antiqua et medievali,<BR>antiquitate classica, et Italia centrali.<BR><B><FONT COLOR=009900>CLICCARE SUPER VINCULAM<BR>AD PAGINAM PRINCIPALEM<BR>VIDENDAM.</SPAN></B><BR><I>(HAC in fenestra<BR>aperietur pagina.)</I>", 
"<P CLASS=center>Deze site omvat ongeveer 15.000 pagina's tekst en foto's, meestal over de Amerikaanse geschiedenis, het oude Rome, de klassieke oudheid, en Midden-Italië.<BR><B><FONT COLOR=009900>KLIK OP DE LINK VOOR DE HOMEPAGE.</SPAN></B><BR><I>(Opent in DIT venster.)</I>", 
"<P CLASS=center>Este site contém cerca de 15.000 páginas de texto e fotos, especialmente sobre a história das Américas, a Roma antiga e medieval, e o centro da Itália.<BR><B><FONT COLOR=009900>CLIQUE NO LINK PARA A PÁGINA DE ACOLHIMENTO.</SPAN></B><BR><I>(A página abre NESTA janela.)</I>", 
"<P CLASS=center>Este sitio contiene aproximadamente 15.000 páginas de texto e fotos, sobre todo sobre la história de las Américas, Roma antigua y medieval, y el centro de Italia.<BR><B><FONT COLOR=009900>CLIC EN EL ENLACE PARA LA PÁGINA PRINCIPAL.</SPAN></B><BR><I>(La página abre en ESTA ventana.)</I>", 
" ", 
" ", 
" ", 
"<P CLASS=center>This site comprises roughly 15,000 pages of text and photos, mostly about American history, ancient Rome, classical Antiquity, and central Italy.<BR><B><FONT COLOR=009900>CLICK HERE FOR THE HOMEPAGE.</SPAN></B><BR>(Opens in another window.)", 
"<P CLASS=center>Ce site comporte environ 15.000 pages de texte et de photos, surtout sur Rome antique et médiévale et l\'Italie centrale.<BR><B><FONT COLOR=009900>FAIRE CLIC ICI POUR LA PAGE D\'ACCUEIL.</SPAN></B><BR>(S\'ouvre dans une autre fenêtre.)", 
"<P CLASS=center>Questo sito contiene circa 15.000 pagine di testo e di foto, innanzitutto sulla Roma antica e medioevale e l\'Italia centrale.<BR><B><FONT COLOR=009900>CLICCARE QUI PER LA PAGINA HOME.</SPAN></B><BR>(Si apre in un altro pannello.)", 
"<P CLASS=center>Hic situs milia paginarum<BR>textus photographiarumque<BR>continet, plerumque<BR>de historia Americana,<BR>Roma antiqua et medievali,<BR>antiquitate classica, et Italia centrali.<BR><B><FONT COLOR=009900>CLICCARE HIC<BR>AD PAGINAM PRINCIPALEM<BR>VIDENDAM.</SPAN></B><BR>(In altera fenestra<BR>aperietur pagina.)", 
"<P CLASS=center>Deze site omvat ongeveer 15.000 pagina's tekst en foto's, meestal over de Amerikaanse geschiedenis, het oude Rome, de klassieke oudheid, en Midden-Italië.<BR><B><FONT COLOR=009900>KLIK OP DE LINK VOOR DE HOMEPAGE.</SPAN></B><BR><I>(Opent in DIT venster.)</I>", 
"<P CLASS=center>Este site contém cerca de 15.000 páginas de texto e fotos, especialmente sobre a Roma antiga e medieval, a história das Américas, e o centro da Itália.<BR><B><FONT COLOR=009900>CLIQUE NO LINK PARA A PÁGINA DE ACOLHIMENTO.</SPAN></B><BR><I>(A página abre em outra janela.)</I>", 
"<P CLASS=center>Este sitio contiene aproximadamente 15.000 páginas de texto e fotos, sobre todo sobre la história de las Américas, Roma antigua y medieval, y el centro de Italia.<BR><B><FONT COLOR=009900>HAGA CLIC AQUÍ PARA LA PÁGINA PRINCIPAL.</SPAN></B><BR><I>(La página abre en una otra ventana.)</I>", 
" ", 
" ", 
" ", 
"<P CLASS=center>Click here to send me an e-mail; you\'ll first get a FAQ covering some of the commoner questions.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"m\'envoyer une e-mail; vous verrez d\'abord un FAQ traitant de quelques questions couramment posées.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"mandarmi un\' e-mail; vedrete prima un FAQ trattando di alcune frequenti questioni.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
"<P CLASS=center>Click here to send me an e-mail; you\'ll first get a FAQ covering some of the commoner things people write me about.<BR><I>(Altera in fenestra aperietur)</I>", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
EClickHere+"the appropriate section of this page.<BR><B><FONT COLOR=FF0000>LET THE PAGE LOAD COMPLETELY BEFORE CLICKING.</SPAN></B>", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
EClickHere+"the author\'s note at the bottom of this page.", 
FClickHere+"la note de l\'auteur au bas de cette page.", 
IClickHere+"la nota<BR>dell\' autore a piè di pagina.", 
" ", 
" ", 
EClickHere+"the editor\'s note at the bottom of this page.", 
FClickHere+"la note de l\'éditeur au bas de cette page.", 
IClickHere+"la nota<BR>dell\' editore a piè di pagina.", 
"<P CLASS=center>Cliccare hic ad editoris notam legendam in ima pagina.", 
" ", 
EClickHere+"a textual note at the bottom of this page.", 
" ", 
IClickHere+"una nota testuale<BR>a piè di pagina.", 
" ", 
" ", 
EClickHere+"the Italian original<BR>of this passage.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
" ", 
" ", 
" ", 
" ", 
"<P CLASS=center>Click here to go one level up:<BR><SPAN CLASS=alert>Opens in THIS window.</SPAN>", 
"<P CLASS=center>Faire clic ici<BR>pour remonter d\'un niveau<BR><SPAN CLASS=alert>(S\'ouvre dans CETTE fenêtre.)</SPAN>", 
"<P CLASS=center>Fare clic qui per risalire un livello<BR><SPAN CLASS=alert>(Si apre in QUESTO pannello.)</SPAN>", 
"<P CLASS=center>Cliccare hic ad paginam superiorem ingrediendam<BR><SPAN CLASS=alert>(HAC in fenestra aperietur.)</SPAN>", 
SClickHere+"ir al nivel superior<BR><SPAN CLASS=alert>(Abre en ESTA ventana)</SPAN>", 
" ", 
" ", 
" ", 
" ", 
" ", 
"<P CLASS=center>Click here to go one level up<BR><I>(Opens in another window.)</I>", 
FClickHere+"remonter d\'un niveau<BR><I>(S\'ouvre dans une autre fenêtre.)</I>", 
"<P CLASS=center>Fare clic qui per risalire un livello<BR><I>(Si apre in un altro pannello.)</I>", 
"<P CLASS=center>Cliccare hic ad paginam superiorem ingrediendam<BR><I>(Altera in fenestra aperietur.)</I>", 
PClickHere+"subir um nivel<BR><I>(Abre em uma outra janela)</I>", 
SClickHere+"ir al nivel superior<BR><I>(Abre en una otra ventana)</I>", 
" ", 
" ", 
" ", 
" ", 
EClickHere+"the passage<BR>in an English translation of Sallust,<BR>linked to the <SPAN CLASS=Latin>Latin</SPAN> text. <BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"le passage<BR>dans une traduction anglaise de Salluste,<BR>lié au texte <SPAN CLASS=Latin>latin</SPAN>. <BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"il passo<BR>in una traduzione inglese di Sallustio,<BR>collegato al testo latino.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
" ", 
EClickHere+"the passage<BR>in the <SPAN CLASS=Latin>Latin</SPAN> text of Sallust,<BR>linked to an English translation. <BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"le passage<BR>dans le texte <SPAN CLASS=Latin>latin</SPAN> de Salluste,<BR>lié à une traduction anglaise. <BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"il passo<BR>nel testo latino di Sallustio,<BR>collegato ad una traduzione in inglese.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
" ", 
EClickHere+"the passage<BR>in an English translation of Tacitus.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"le passage<BR>dans une traduction anglaise de Tacite.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"il passo<BR>in una traduzione inglese di Tacito.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
"<P CLASS=center>Haga clic aquí por el pasaje<BR>en una traducción inglesa de Tacito.<BR><I>(Abre en una otra ventana)</I>", 
EClickHere+"the passage<BR>in the <SPAN CLASS=Latin>Latin</SPAN> text of Tacitus,<BR>linked to an English translation. <BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"le passage<BR>dans le texte <SPAN CLASS=Latin>latin</SPAN> de Tacite,<BR>lié à une traduction anglaise. <BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"il passo<BR>nel testo latino di Tacito,<BR>collegato ad una traduzione in inglese.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
"<P CLASS=center>Haga clic aquí por el pasaje<BR>en el texto latino de Tacito.<BR><I>(Abre en una otra ventana)</I>", 
EClickHere+"the Bible verse<BR>in <SPAN CLASS=Greek>Greek</SPAN>, <SPAN CLASS=Latin>Latin</SPAN>, <SPAN CLASS=source>English</SPAN> facing columns.<BR><I>(Offsite, opens in another window)</I>", 
" ", 
" ", 
" ", 
PClickHere+"o versículo da Bíblia<BR>em colunas enfrentadas: <SPAN CLASS=Greek>grego</SPAN>, <SPAN CLASS=Latin>latim</SPAN>, <SPAN CLASS=source>inglês</SPAN>.<BR><I>(Offsite: a página abre em uma outra janela)</I>", 
"<P CLASS=center><B>CULLUM NUMBER</B><BR><I>(If you don\'t know what this is,<BR>click here for an explanation<BR>on the Cullum\'s Register homepage:<BR>opens in another window.)</I>", 
"<P CLASS=center><B>CLASS RANK</B><BR><I>From 1818 to 1977, within each Class graduates are listed in order of their general merit: academic and military standing combined.</I>", 
" ", 
" ", 
" ", 
"<P CLASS=center><I>(De pagina opent in DIT venster)</I>", 
"<P CLASS=center><I>(De pagina opent in een ander venster)</I>", 
"<P CLASS=center><I>(Offsite: de pagina opent in een ander venster)</I>", 
"<P CLASS=center><I>(Deze foto of een verwante foto, opent in een ander venster)</I>", 
"<P CLASS=center><I>(De foto wordt geopend in een ander venster)</I>", 
"<P CLASS=center><I>(Elders op deze pagina)</I>", 
NClickHere+"de nota van de auteur aan de onderkant van deze pagina.", 
NClickHere+"mijn nota aan de onderkant van deze pagina.", 
"<P CLASS=center>Klik hier om terug te gaan <BR> de verwijzing in de tekst.", 
"<P CLASS=center>Als je niet weet waar dit over gaat, <BR> je alleen maar een klik verwijderd van de uitleg.<BR><I>(Opent in een ander venster)</I>", 
"<P CLASS=center><I>Klik hier om een niveau omhoog gaan.<BR>(Opent in DIT venster)</I>", 
"<P CLASS=center><I>Klik hier om een niveau omhoog gaan.<BR>(Opent in een ander  venster)</I>", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
EClickHere+"the passage<BR>in a <SPAN CLASS=Latin>Latin</SPAN> translation of Aelian.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"le passage<BR>dans une traduction <SPAN CLASS=Latin>latine</SPAN> d\'Elien.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"il passo<BR>in una traduzione <SPAN CLASS=Latin>latina</SPAN>  di Eliano.<BR><I>(Si apre in un altro pannello)</I>", 
" ", 
SClickHere+"el pasaje<BR>en una traducción <SPAN CLASS=Latin>latina</SPAN> de Eliano.<BR><I>(Abre en una otra ventana)</I>", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
EClickHere+"the passage<BR>in the Greek text.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"le passage du texte grec.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"il passo dell\' autore greco.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
SClickHere+"el pasaje del autor griego.<BR><I>(Abre en una otra ventana)</I>", 
EClickHere+"the passage<BR>in the Greek text,<BR>linked to a translation<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"le passage du texte grec.<BR>liée à une traduction<SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"il passo dell\' autore greco.<BR>collegato ad una traduzione<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
" ", 
SClickHere+"el pasaje del autor griego.<BR>con enlace a una traducción<I>(Abre en una otra ventana)</I>", 
EClickHere+"the passage<BR>in the Greek text.<BR><I>(Offsite: opens in another window)</I>", 
FClickHere+"le passage du texte grec.<BR><I>(Hors site: s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il passo dell\' autore greco.<BR><I>(Fuori sito: si apre in un altro pannello)</I>", 
" ", 
SClickHere+"el pasaje del autor griego.<BR><I>(Fuera del sitio: abre en una otra ventana)</I>", 
EClickHere+"the passage<BR>in the Greek text,<BR>linked to a translation<BR><I>(Offsite: opens in another window)</I>", 
FClickHere+"le passage du texte grec.<BR>liée à une traduction<I>(Hors site: s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il passo dell\' autore greco.<BR>collegato ad una traduzione<BR><I>(Fuori sito: si apre in un altro pannello)</I>", 
" ", 
SClickHere+"el pasaje del autor griego.<BR>con enlace a una traducción<I>(Fuera del sitio: abre en una otra ventana)</I>", 
EClickHere+"the passage<BR>in an English translation<BR>linked to the original <SPAN CLASS=Greek>Greek</SPAN>.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I></CENTER>", 
FClickHere+"le passage<BR>en traduction anglaise<BR>lié au texte <SPAN CLASS=Greek>grec</SPAN>.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"il passo<BR>in una traduzione inglese<BR>collegato al testo greco.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN></CENTER>", 
"<P CLASS=center>Cliccare hic ad legendum<BR>in anglica versione<BR>ad Graecum textum conexum.<BR><I>(Altera in fenestra aperietur pagina)</I>", 
SClickHere+"este pasaje<BR>en una traducción inglesa<BR>con enlace al texto greco.<BR><I>(Abre en una otra ventana)</I>", 
EClickHere+"the passage<BR>in an English translation<BR>linked to the original <SPAN CLASS=Greek>Greek</SPAN>.<BR><I>(Offsite, opens in another window)</I></CENTER>", 
FClickHere+"le passage<BR>en traduction anglaise<BR>lié au texte <SPAN CLASS=Greek>grec</SPAN>.<BR><I>(Hors site, s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il passo<BR>in una traduzione inglese<BR>collegato al testo <SPAN CLASS=Greek>greco</SPAN>.<BR><I>(Fuori sito, si apre in un altro pannello)</I></CENTER>", 
"<P CLASS=center>Cliccare hic ad legendum<BR>in anglica versione<BR>ad Graecum textum conexum.<BR><I>(Apud alios, altera in fenestra aperietur pagina)</I>", 
SClickHere+"este pasaje<BR>en una traducción inglesa<BR>con enlace al texto <SPAN CLASS=Greek>greco</SPAN>.<BR><I>(Fuera del sitio, abre en una otra ventana)</I>", 
EClickHere+"the passage<BR>in the original <SPAN CLASS=Greek>Greek</SPAN><BR>linked to an English translation.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I></CENTER>", 
FClickHere+"le passage<BR>dans le texte <SPAN CLASS=Greek>grec</SPAN><BR>lié à une traduction anglaise.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"il passo<BR>nel testo greco<BR>collegato ad una traduzione inglese.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN></CENTER>", 
"<P CLASS=center>Cliccare hic ad legendum<BR>Graecum textum<BR>ad anglicam versionem conexum.<BR><I>(Altera in fenestra aperietur pagina)</I>", 
SClickHere+"este pasaje<BR>en el texto greco<BR>con enlace a una traducción inglesa.<BR><I>(Abre en una otra ventana)</I>", 
EClickHere+"the passage<BR>in the original <SPAN CLASS=Greek>Greek</SPAN><BR>linked to an English translation.<BR><I>(Offsite, opens in another window)</I></CENTER>", 
FClickHere+"le passage<BR>dans le texte <SPAN CLASS=Greek>grec</SPAN><BR>lié à une traduction anglaise.<BR><I>(Hors site, s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il passo<BR>nel testo greco<BR>collegato ad una traduzione inglese.<BR><I>(Fuori sito, si apre in un altro pannello)</I></CENTER>", 
"<P CLASS=center>Cliccare hic ad legendum<BR>Graecum textum<BR>ad anglicam versionem conexum.<BR><I>(Apud alios, altera in fenestra aperietur pagina)</I>", 
SClickHere+"este pasaje<BR>en el texto greco<BR>con enlace a una traducción inglesa.<BR><I>(Fuera del sitio, abre en una otra ventana)</I>", 
EClickHere+"the passage in Plutarch<BR>in an English translation<BR>linked to the original <SPAN CLASS=Greek>Greek</SPAN><BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"le passage dans Plutarque<BR>en traduction anglaise<BR>lié au texte <SPAN CLASS=Greek>grec</SPAN><I>(S\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il passo in Plutarco<BR><BR>in una traduzione inglese<BR>collegato al testo <SPAN CLASS=Greek>greco</SPAN>.<BR><I>(Si apre in un altro pannello)</I>", 
" ", 
SClickHere+"el pasaje en Plutarco<BR>en una traducción inglesa<BR>con enlace al texto <SPAN CLASS=Greek>greco</SPAN>.<BR><I>(en inglés, abre en una otra ventana)</I>", 
EClickHere+"the passage in the Res Gestae<BR>— parallel texts:<BR><SPAN CLASS=Latin>Latin</SPAN>, <SPAN CLASS=Greek>Greek</SPAN>, <SPAN CLASS=English>English</SPAN><BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
" ", 
" ", 
" ", 
" ", 
"<P CLASS=center><I>Link is to the Livius.Org website:<BR>page opens in<BR>another window.</I>", 
EClickHere+"Jona Lendering\'s note at the bottom of this page.", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
EClickHere+"the passage<BR>in the original <SPAN CLASS=Latin>Latin</SPAN><BR>linked to a French translation.<BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I></CENTER>",  //"THIS IS WHAT REALLY BELONGS IN 510:<CENTER>Click here for the passage<BR>in the <SPAN CLASS=Latin>Latin</SPAN> text of Suetonius,<BR>linked to an English translation. <BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"le passage<BR>dans le texte <SPAN CLASS=Latin>latin</SPAN><BR>lié à une traduction française.<BR><SPAN CLASS=alert>(S'ouvre dans une autre fenêtre)</SPAN>", 
IClickHere+"il passo<BR>nel testo latino<BR>collegato ad una traduzione francese.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN></CENTER>", //"THIS IS WHAT REALLY BELONGS IN 512:<CENTER>Cliccare qui per il passo<BR>nel testo latino di Svetonio,<BR>collegato a traduzioni in inglese e francese.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
"<P CLASS=center>Cliccare hic ad legendum<BR>Latinum textum<BR>ad anglicam versionem conexum.<BR><I>(Altera in fenestra aperietur pagina)</I>", 
SClickHere+"este pasaje<BR>en el texto latino<BR>con enlace a una traducción francesa.<BR><I>(Abre en una otra ventana)</I>", 
EClickHere+"the passage<BR>in the original <SPAN CLASS=Latin>Latin</SPAN><BR>linked to a French translation.<BR><I>(Offsite, opens in another window)</I></CENTER>",  //"THIS IS WHAT REALLY BELONGS IN 515:<CENTER>Click here for the passage<BR>in the <SPAN CLASS=Latin>Latin</SPAN> text of Suetonius,<BR>linked to an English translation. <BR><I><SPAN CLASS=whole>(Opens in another window)</SPAN></I>", 
FClickHere+"le passage<BR>dans le texte <SPAN CLASS=Latin>latin</SPAN><BR>lié à une traduction française.<BR><I>(Hors site, s\'ouvre dans une autre fenêtre)</I>", 
IClickHere+"il passo<BR>nel testo latino<BR>collegato ad una traduzione francese.<BR><I>(Fuori sito, si apre in un altro pannello)</I></CENTER>", //"THIS IS WHAT REALLY BELONGS IN 517:<CENTER>Cliccare qui per il passo<BR>nel testo latino di Svetonio,<BR>collegato a traduzioni in inglese e francese.<BR><SPAN CLASS=alert>(Si apre in un altro pannello)</SPAN>", 
"<P CLASS=center>Cliccare hic ad legendum<BR>Latinum textum<BR>ad Francogallicam versionem conexum.<BR><I>(Apud alios, altera in fenestra aperietur pagina)</I>", 
SClickHere+"este pasaje<BR>en el texto latino<BR>con enlace a una traducción francesa.<BR><I>(Fuera del sitio, abre en una otra ventana)</I>", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
" ", 
"<P CLASS=center><B><FONT COLOR=009900>THIS IS THE PAGE YOU\'RE ON.</SPAN></B>", 
"<P CLASS=center><B><FONT COLOR=009900>C\'EST LA PAGE QUE VOUS AVEZ DEVANT LES YEUX.</SPAN></B>", 
"<P CLASS=center><B><FONT COLOR=009900>QUESTA È LA PAGINA CHE AVETE DAVANTI AGLI OCCHI.</SPAN></B>", 
" ", 
" ", 
"<P CLASS=center><FONT COLOR=FF0000>ACTIVE AREAS:</SPAN><BR>WHEREVER THIS PROMPT<BR>IS REPLACED BY ANOTHER", 
"<P CLASS=center><FONT COLOR=FF0000>ZONES ACTIVES :</SPAN><BR>PARTOUT OU CE MESSAGE EST REMPLACE PAR UN AUTRE", 
"<P CLASS=center><FONT COLOR=FF0000>AREE ATTIVE:</SPAN><BR>OVUNQUE QUESTO MESSAGGIO VIENE SOSTITUITO DA UN\' ALTRO", 
"<P CLASS=center><FONT COLOR=000000>Click here for the homepage of the<BR><B>U. S. MILITARY ACADEMY.</B><BR><I>(Offsite: opens in another window.)</I></SPAN>", 
"<P CLASS=center><FONT COLOR=0033FF>Click here for the homepage of the<BR><B>U. S. NAVAL ACADEMY.</B><BR><I>(Offsite: opens in another window.)</I></SPAN>", 
"<P CLASS=center><FONT COLOR=0033FF>Click here for the homepage of the<BR><B>U. S. COAST GUARD ACADEMY.</B><BR><I>(Offsite: opens in another window.)</I></SPAN>", 

" " //THIS LAST LINE MUST NOT END WITH A COMMA
);//END ARRAY; start is at START ARRAY

// Array with captions.
var ol_caps = new Array("Array Caption 0", "Array Caption 1");



////////////////////////////////////
// END CONFIGURATION
////////////////////////////////////



////////////////////////////////////
// INIT
////////////////////////////////////


// Runtime variables init. Used for runtime only, don't change, not for config!
var o3_text = "";
var o3_cap = "";
var o3_sticky = 0;
var o3_background = "";
var o3_close = "Close";
var o3_hpos = RIGHT;
var o3_offsetx = 2;
var o3_offsety = -3;
var o3_fgcolor = "";
var o3_bgcolor = "";
var o3_textcolor = "";
var o3_capcolor = "";
var o3_closecolor = "";
var o3_width = 100;
var o3_border = 1;
var o3_status = "";
var o3_autostatus = 0;
var o3_height = -1;
var o3_snapx = 0;
var o3_snapy = 0;
var o3_fixx = -1;
var o3_fixy = -1;
var o3_fgbackground = "";
var o3_bgbackground = "";
var o3_padxl = 0;
var o3_padxr = 0;
var o3_padyt = 0;
var o3_padyb = 0;
var o3_fullhtml = 0;
var o3_vpos = ABOVE;
var o3_aboveheight = 3;
var o3_capicon = "";
var o3_textfont = "Verdana,Arial,Helvetica";
var o3_captionfont = "Verdana,Arial,Helvetica";
var o3_closefont = "Verdana,Arial,Helvetica";
var o3_textsize = "1";
var o3_captionsize = "1";
var o3_closesize = "1";
var o3_frame = self;
var o3_timeout = 0;
var o3_timerid = 0;
var o3_allowmove = 0;
var o3_function = Function();
var o3_delay = 0;
var o3_delayid = 0;
var o3_hauto = 0;
var o3_vauto = 0;

// OTHER THAYER VARIABLES
var BadF = "<BR><SPAN CLASS=goof>";
var GreekF = "<BR><SPAN CLASS=Greek>";
var LatinF = "<BR><SPAN CLASS=Latin>";
var SearchF = "<BR><SPAN CLASS=searchand>";


var TypeErr = "<P CLASS=center>The typescript has<BR><SPAN CLASS=goof>";
var SourceErr = "<P CLASS=center>The printed text has<BR><SPAN CLASS=goof>";
var SourceOm = "<P CLASS=center>The printed text omits<BR><SPAN CLASS=searchand>";
var SourceOmL = "<P CLASS=center>The printed text omits<BR><SPAN CLASS=Latin>";
var SourceOmG = "<P CLASS=center>The printed text omits<BR><SPAN CLASS=Greek>";
var SourceOm0 = "<P CLASS=center>The printed text<BR>omits this.";
var SourceOm1 = "<P CLASS=center>The printed text<BR>omits this word.";
var SourceOm2 = "<P CLASS=center>The printed text<BR>omits these words/this passage.";


var FrTypeErr = "<P CLASS=center>Le tapuscrit porte<BR><SPAN CLASS=goof>";
var FrSourceErr = "<P CLASS=center>Le texte imprimé porte<BR><SPAN CLASS=goof>";
var FrSourceOm = "<P CLASS=center>Le texte imprimé omet<BR><SPAN CLASS=searchand>";
var FrSourceOmL = "<P CLASS=center>Le texte imprimé omet<BR><SPAN CLASS=Latin>";
var FrSourceOmG = "<P CLASS=center>Le texte imprimé omet<BR><SPAN CLASS=Greek>";

var FrSourceOm1 = "<P CLASS=center>Le texte imprimé omet ce mot.";
var FrSourceOm2 = "<P CLASS=center>Le texte imprimé omet ces mots/ce passage.";


var ItTypeErr = "<P CLASS=center>Il dattiloscritto reca<BR><SPAN CLASS=goof>";
var ItSourceErr = "<P CLASS=center>Il testo stampato reca<BR><SPAN CLASS=goof>";
var ItSourceOm = "<P CLASS=center>Il testo stampato omette<BR><SPAN CLASS=searchand>";
var ItSourceOmL = "<P CLASS=center>Il testo stampato omette<BR><SPAN CLASS=Latin>";
var ItSourceOmG = "<P CLASS=center>Il testo stampato omette<BR><SPAN CLASS=Greek>";
var ItSourceOm0 = "<P CLASS=center>Il testo stampato<BR>omette questo.";
var ItSourceOm1 = "<P CLASS=center>Il testo stampato<BR>omette questa parola.";
var ItSourceOm2 = "<P CLASS=center>Il testo stampato<BR>omette queste parole/questo passo.";



var NeSourceErr = "<P CLASS=center>In de gedrukte tekst leest<BR><SPAN CLASS=goof>";
var NeSourceOm = "<P CLASS=center>De gedrukte tekst weglaat<BR><SPAN CLASS=searchand>";








var PgSourceOm0 = "<P CLASS=center>O texto impresso omite isso.";
var PgSourceErr = "<P CLASS=center>No texto impresso lê‑se<BR><SPAN CLASS=goof>";
var PgSourceOm = "<P CLASS=center>O texto impresso omite<BR><SPAN CLASS=searchand>";
var PgSourceOmL = "<P CLASS=center>O texto impresso omite<BR><SPAN CLASS=Latin>";
var PgSourceOmG = "<P CLASS=center>O texto impresso omite<BR><SPAN CLASS=Greek>";





var SpSourceErr = "<P CLASS=center>En el texto imprimido<BR>se lee<BR><SPAN CLASS=goof>";
var SpSourceOm = "<P CLASS=center>El texto imprimido omite<BR><SPAN CLASS=searchand>";
var SpSourceOmL = "<P CLASS=center>El texto imprimido omite<BR><SPAN CLASS=Latin>";
var SpSourceOmG = "<P CLASS=center>El texto imprimido omite<BR><SPAN CLASS=Greek>";

var MyDiaryErr = "<P CLASS=center>In my diary, I wrote<BR><SPAN CLASS=goof>";




var SourceErrMe = "<P CLASS=center>I actually wrote<BR><SPAN CLASS=goof>";
var SourceOmMe = "<P CLASS=center>I omitted<BR><SPAN CLASS=searchand>";

var DivergenceFromLatin = "<P CLASS=center>The Latin text onsite is not the one on which this translation is based. It reads<BR><SPAN CLASS=goof>";
var DivergenceFromGreek = "<P CLASS=center>The Latin text onsite is not the one on which this translation is based. It reads<BR><SPAN CLASS=goof>";
var DivergenceInEnglish = "<P CLASS=center>The English translation onsite is not based on this text. It reads<BR><SPAN CLASS=goof>";

var CloseF = "</SPAN>";
var USMAPromptWidth = 205;
var USNAPromptWidth = 205;
var USCGAPromptWidth = 205;
var PDFPromptWidth = 216;
var DiaryErr = "<P CLASS=center>The diary actually reads<BR><SPAN CLASS=goof>";
var DiaryOm = "<P CLASS=center>The diary omits<BR><SPAN CLASS=searchand>";

var Ru2 = "<P CLASS=center><I>Ссылка выключен сайт:<BR>страница открывается в другом окне</I>";



// THAYER'S ARRAY. (add 355 for the linenum of the corresponding text)
var ThisPhoto = 3;
var Photo = 4;
var OnPage = 5;
var Note = 6;
var MyNote = 7;
var BackRef = 8;
var Glossary = 9;

var Ca0 = 420; var CaWidth0 = 210;
var Ca1 = 421; var CaWidth1 = 210;
var Ca2 = 422; var CaWidth2 = 140;
var CaThisPhoto = 423; var CaThisPhotoWidth = 180;
var CaPhoto = 424;
var CaOnPage = 425; var CaOnPageWidth = 150;
var CaNote = 426;
var CaMyNote = 427;
var CaBackRef = 428;
var CaGlossary = 429;

var Fr0 = 10; var FrWidth0 = 180;
var Fr1 = 11; var FrWidth1 = 210;
var Fr2 = 12;
var FrThisPhoto = 13;
var FrPhoto = 14;
var FrOnPage = 15;
var FrNote = 16;
var FrMyNote = 17;
var FrBackRef = 18;
var FrGlossary = 19;

var Ge0 = 20;
var Ge1 = 21;
var Ge2 = 22;
var GeThisPhoto = 23;
var GePhoto = 24;
var GeOnPage = 25;
var GeNote = 26;
var GeMyNote = 27;
var GeBackRef = 28;
var GeGlossary = 29;

var It0 = 30; var ItWidth0 = 210;
var It1 = 31; var ItWidth1 = 210;
var It2 = 32; var ItWidth2 = 210;
var ItThisPhoto = 33; var ItThisPhotoWidth = 180;
var ItPhoto = 34;
var ItOnPage = 35; var ItOnPageWidth = 150;
var ItNote = 36;
var ItMyNote = 37;
var ItBackRef = 38;
var ItGlossary = 39;

var La0 = 40;
var La1 = 41;
var La2 = 42;
var LaThisPhoto = 43;
var LaPhoto = 44;
var LaOnPage = 45;
var LaNote = 46;
var LaMyNote = 47;
var LaGlossary = 49;

var Sp0 = 50; var SpWidth0 = 210;
var Sp1 = 51; var SpWidth1 = 210;
var Sp2 = 52; var SpWidth2 = 140;
var SpThisPhoto = 53; var SpThisPhotoWidth = 180;
var SpPhoto = 54;
var SpOnPage = 55; var SpOnPageWidth = 150;
var SpNote = 56;
var SpMyNote = 57;
var SpBackRef = 58;
var SpGlossary = 59;

var Pt0 = 90; var PtWidth0 = 210;
var Pt1 = 91; var PtWidth1 = 210;
var Pt2 = 92; var PtWidth2 = 140;
var PtThisPhoto = 93; var PtThisPhotoWidth = 180;
var PtPhoto = 94;
var PtOnPage = 95; var PtOnPageWidth = 190;
var PtNote = 96;
var PtMyNote = 97;
var PtBackRef = 98;
var PtGlossary = 99;

var Smith0 = 60; var SmithWidth0 = 200;
var FrSmith0 = 61;
var ItSmith0 = 62;
var SpSmith0 = 64;
var Smith1 = 65; var SmithWidth1 = 200;
var FrSmith1 = 66;
var ItSmith1 = 67;
var SpSmith1 = 69;

var Glossary0 = 70;
var FrGlossary0 = 71;
var ItGlossary0 = 72;

var Glossary2 = 75;
var FrGlossary2 = 76;
var ItGlossary2 = 77;

var SmithSub0 = 80;
var FrSmithSub0 = 81;
var ItSmithSub0 = 82;
var SpSmithSub0 = 84;

var SmithSub1 = 85; var SmithSubWidth1 = 190;
var FrSmithSub1 = 86;
var ItSmithSub1 = 87;
var SpSmithSub1 = 89;

var XMarksTheSpot = 790;
var FrXMarksTheSpot = 791;
var ItXMarksTheSpot = 792;

var ActiveAreas = 795;
var FrActiveAreas = 796;
var ItActiveAreas = 797;

var USMA = 798;
var USNA = 799;
var USCGA = 800;

var SmithHome = 100;
var FrSmithHome = 101;
var ItSmithHome = 102;
var SpSmithHome = 104;
var TextOnPage = 106;
var SmithHome0 = 107;
var DarembergHome = 108;
var DarembergHome0 = 109;

var Platner0 = 110;
var FrPlatner0 = 111;
var ItPlatner0 = 112;
var LaPlatner0 = 113;
var SpPlatner0 = 114;
var Platner1 = 115;
var FrPlatner1 = 116;
var ItPlatner1 = 117;
var LaPlatner1 = 118;
var SpPlatner1 = 119;

var PlatnerPhoto0 = 120;
var FrPlatnerPhoto0 = 121;
var ItPlatnerPhoto0 = 122;
var LaPlatnerPhoto0 = 123;
var SpPlatnerPhoto0 = 124;
var PlatnerPhoto1 = 125;
var FrPlatnerPhoto1 = 126;
var ItPlatnerPhoto1 = 127;
var LaPlatnerPhoto1 = 128;
var SpPlatnerPhoto1 = 129;

var PlatnerSub0 = 130;
var FrPlatnerSub0 = 131;
var ItPlatnerSub0 = 132;
var SpPlatnerSub0 = 134;
var PlatnerSub1 = 135;
var FrPlatnerSub1 = 136;
var ItPlatnerSub1 = 137;
var SpPlatnerSub1 = 139;

var CompleteWork0 = 140;
var FrCompleteWork0 = 141;
var ItCompleteWork0 = 142;
var SpCompleteWork0 = 144;
var CompleteWork1 = 145;
var FrCompleteWork1 = 146;
var ItCompleteWork1 = 147;
var SpCompleteWork1 = 149;

var Armellini0 = 150;
var FrArmellini0 = 151;
var ItArmellini0 = 152;
var SpArmellini0 = 154;
var Armellini1 = 155;
var FrArmellini1 = 156;
var ItArmellini1 = 157;
var SpArmellini1 = 159;

var Huelsen0 = 160;
var FrHuelsen0 = 161;
var ItHuelsen0 = 162;
var SpHuelsen0 = 164;
var Huelsen1 = 165;
var FrHuelsen1 = 166;
var ItHuelsen1 = 167;
var SpHuelsen1 = 169;

var RomeChurch0 = 170;
var FrRomeChurch0 = 171;
var ItRomeChurch0 = 172;
var SpRomeChurch0 = 174;
var RomeChurch1 = 175;
var FrRomeChurch1 = 176;
var ItRomeChurch1 = 177;
var SpRomeChurch1 = 179;

var Daremberg0 = 180;
var FrDaremberg0 = 181;
var ItDaremberg0 = 182;
var SpDaremberg0 = 184;
var Daremberg1 = 185;
var FrDaremberg1 = 186;
var ItDaremberg1 = 187;
var SpDaremberg1 = 189;

var Page0 = 190;
var FrPage0 = 191;
var ItPage0 = 192;
var LaPage0 = 193;
var SpPage0 = 194;
var Page1 = 195;
var FrPage1 = 196;
var ItPage1 = 197;
var LaPage1 = 198;
var SpPage1 = 199;

var Pages0 = 200;
var FrPages0 = 201;
var ItPages0 = 202;
var LaPages0 = 203;
var SpPages0 = 204;
var Pages1 = 205;
var FrPages1 = 206;
var ItPages1 = 207;
var LaPages1 = 208;
var SpPages1 = 209;

var ChurchPage0 = 210;
var FrChurchPage0 = 211;
var ItChurchPage0 = 212;
var LaChurchPage0 = 213;
var SpChurchPage0 = 214;
var ChurchPage1 = 215;
var FrChurchPage1 = 216;
var ItChurchPage1 = 217;
var LaChurchPage1 = 218;
var SpChurchPage1 = 219;

var ChurchPages0 = 220;
var FrChurchPages0 = 221;
var ItChurchPages0 = 222;
var LaChurchPages0 = 223;
var SpChurchPages0 = 224;
var ChurchPages1 = 225;
var FrChurchPages1 = 226;
var ItChurchPages1 = 227;
var LaChurchPages1 = 228;
var SpChurchPages1 = 229;

var Town0 = 230;
var FrTown0 = 231;
var ItTown0 = 232;
var LaTown0 = 233;
var SpTown0 = 234;
var Town1 = 235;
var FrTown1 = 236;
var ItTown1 = 237;
var LaTown1 = 238;
var SpTown1 = 239;

var EPlusL = 240;
var FrEPlusL = 241;
var ItEPlusL = 242;
var SpEPlusL = 244;
var EPlusL2 = 245;
var FrEPlusL2 = 246;
var ItEPlusL2 = 247;
var LaEPlusL2 = 248;
var SpEPlusL2 = 249;

var LPlusE = 250;
var FrLPlusE = 251;
var ItLPlusE = 252;
var SpLPlusE = 254;
var LPlusE2 = 255;
var FrLPlusE2 = 256;
var ItLPlusE2 = 257;
var SpLPlusE2 = 259;

var Pliny = 260;
var FrPliny = 261;
var ItPliny = 262;
var SpPliny = 264;

var Ptolemy = 265;
var FrPtolemy = 266;
var ItPtolemy = 267;
var LaPtolemy = 268;

var Ammian = 270;
var FrAmmian = 271;
var ItAmmian = 272;

var Appian = 275;
var FrAppian = 276;
var ItAppian = 277;

var Dio = 280;
var FrDio = 281;
var ItDio = 282;
var SpDio = 284;

var Plutarch = 285; var PlutarchWidth = 230;
var FrPlutarch = 286;
var ItPlutarch = 287;
var SpPlutarch = 289;

var Polybius = 290;
var FrPolybius = 291;
var ItPolybius = 292;
var LaPolybius = 293;

var Strabo = 295;
var FrStrabo = 296;
var ItStrabo = 297;
var LaStrabo = 298;

var Chiesa0 = 300;
var Chiesa1 = 301;
var Artista0 = 302;
var Artista = 303;
var Catalogo = 304;
var Pianta = 305;
var QuadroPianta = 306;
var ChiesaNelTesto = 307;
var ETitiArtista0 = 308;
var ETitiArtista = 309;

var MySite0 = 310;
var FrMySite0 = 311;
var ItMySite0 = 312;
var SpMySite0 = 314;
var MySite1 = 315;
var FrMySite1 = 316;
var ItMySite1 = 317;
var SpMySite1 = 319;

var MyMidSite0 = 320;
var FrMyMidSite0 = 321;
var ItMyMidSite0 = 322;
var SpMyMidSite0 = 324;
var MyMidSite1 = 325;
var FrMyMidSite1 = 326;
var ItMyMidSite1 = 327;
var SpMyMidSite1 = 329;

var MyBigSite0 = 330;
var FrMyBigSite0 = 331;
var ItMyBigSite0 = 332;
var SpMyBigSite0 = 334;
var MyBigSite1 = 335;
var FrMyBigSite1 = 336;
var ItMyBigSite1 = 337;
var SpMyBigSite1 = 339;

var MyBook0 = 340;
var FrMyBook0 = 341;
var ItMyBook0 = 342;
var LaMyBook0 = 343;
var SpMyBook0 = 344;
var MyBook1 = 345;
var FrMyBook1 = 346;
var ItMyBook1 = 347;
var LaMyBook1 = 348;
var SpMyBook1 = 349;

var TheirSite = 350;
var FrTheirSite = 351;
var ItTheirSite = 352;
var SpTheirSite = 357;

var LatinText = 360;
var FrLatinText = 361;
var ItLatinText = 362;
var SpLatinText = 367;

var LatinRef1 = 370;
var FrLatinRef1 = 371;
var ItLatinRef1 = 372;
var SpLatinRef1 = 374;
var LatinTrans1 = 375;
var FrLatinTrans1 = 376;
var ItLatinTrans1 = 377;
var SpLatinTrans1 = 379;

var LatinRef2 = 380;
var FrLatinRef2 = 381;
var ItLatinRef2 = 382;
var SpLatinRef2 = 384;
var LatinRef2PlusTranslation = 385; //KEEP. Use for texts with translations into languages other than English
var FrLatinRef2PlusTranslation = 386;
var ItLatinRef2PlusTranslation = 387;
var SpLatinRef2PlusTranslation = 389;

var LatinPlus1 = 390;
var FrLatinPlus1 = 391;
var ItLatinPlus1 = 392;
var SpLatinPlus1 = 394;
var LatinPlus2 = 395;
var FrLatinPlus2 = 396;
var ItLatinPlus2 = 397;
var SpLatinPlus2 = 399;

var Original1 = 400;
var FrOriginal1 = 401;
var ItOriginal1 = 402;
var LaOriginal1 = 403;
var SpOriginal1 = 404;
var Original2 = 405;
var FrOriginal2 = 406;
var ItOriginal2 = 407;
var LaOriginal2 = 408;
var SpOriginal2 = 409;

var Translation1 = 410;
var FrTranslation1 = 411;
var ItTranslation1 = 412;
var SpTranslation1 = 414;
var Translation2 = 415;
var FrTranslation2 = 416;
var ItTranslation2 = 417;
var SpTranslation2 = 419;

var PDF = 430;
var FrPDF = 431;
var ItPDF = 432;
var SpPDF = 434;

var JSTOR = 435;
var FrJSTOR = 436;
var ItJSTOR = 437;
var SpJSTOR = 438;

var BadCoding = 440;
var FrBadCoding = 441;
var ItBadCoding = 442;
var SpBadCoding = 444;
var Loud = 445;
var FrLoud = 446;
var ItLoud = 447;
var SpLoud = 448;

var Solution = 450;
var FrSolution = 451;
var ItSolution = 452;
var SpSolution = 454;

var Diodorus = 460;
var FrDiodorus = 461;
var ItDiodorus = 462;
var SpDiodorus = 464;

var Herodotus = 465;
var FrHerodotus = 466;
var ItHerodotus = 467;
var SpHerodotus = 469;

var Pausanias = 470;
var FrPausanias = 471;
var ItPausanias = 472;
var SpPausanias = 474;

var Thucydides = 475;
var FrThucydides = 476;
var ItThucydides = 477;
var SpThucydides = 479;

var FrontinusL = 480;
var FrFrontinusL = 481;
var ItFrontinusL = 482;
var SpFrontinusL = 484;

var FrontinusE = 490;
var FrFrontinusF = 491;

var Dionysius = 495;
var FrDionysius = 496;
var ItDionysius = 497;
var LaDionysius = 498;
var SpDionysius = 499;

var Glossary0 = 500;
var FrGlossary0 = 501;
var ItGlossary0 = 502;
var SpGlossary0 = 507;

var LatinOriginal = 510;
var FrLatinOriginal = 511;
var ItLatinOriginal = 512;
var SpLatinOriginal = 513;

var GreekOriginal = 515;
var FrGreekOriginal = 516;
var ItGreekOriginal = 517;
var SpGreekOriginal = 518;

var Home = 520;
var FrHome = 521;
var ItHome = 522;
var LaHome = 524;
var SpHome = 527;
var Home1 = 530;
var FrHome1 = 531;
var ItHome1 = 532;
var LaHome1 = 533;
var NeHome1 = 534;
var PtHome1 = 535;
var SpHome1 = 536;

var Mail = 540;
var FrMail = 541;
var ItMail = 542;
var LaMail = 543;
var SpMail = 544;

var LetLoad = 550;
var FrLetLoad = 551;
var ItLetLoad = 552;
var LaLetLoad = 553;
var SpLetLoad = 554;

var AuNote = 560;
var FrAuNote = 561;
var ItAuNote = 562;

var EdNote = 565;
var FrEdNote = 566;
var ItEdNote = 567; var ItEdNoteWidth = 230;

var CritNote = 570;
var ItCritNote = 572;

var ItalianOriginal = 575;
var FrItalianOriginal = 576;
var ItItalianOriginal = 577;
var SpItalianOriginal = 578;

var Up = 580;
var FrUp = 581;
var ItUp = 582;
var LaUp = 583;
var SpUp = 584;
var Up1 = 590;
var FrUp1 = 591;
var ItUp1 = 592;
var LaUp1 = 593;
var PtUp1 = 594;
var SpUp1 = 595;

var SallustE = 600;
var FrSallustE = 601;
var ItSallustE = 602;

var SallustL = 605;
var FrSallustL = 606;
var ItSallustL = 607;

var Tacitus = 610;
var FrTacitusE = 611;
var ItTacitusE = 612;
var SpTacitusE = 614;

var TacitusL = 615;
var FrTacitusL = 616;
var ItTacitusL = 617;
var SpTacitusL = 619;

var Bible = 620;
var FrBible = 621;
var ItBible = 622;
var PtBible = 624;
// var SpBible = 624;

var CullumNo = 625;
var CullumRank = 626;

var Ne0 = 630; var NeWidth0 = 190;
var Ne1 = 631; var NeWidth1 = 210;
var Ne2 = 632; var NeWidth2 = 140;
var NeThisPhoto = 633; var NeThisPhotoWidth = 180;
var NePhoto = 634;
var NeOnPage = 635; var NeOnPageWidth = 150;
var NeNote = 636;
var NeMyNote = 637;
var NeBackRef = 638;
var NeGlossary = 639;
var NeUp = 640;
var NeUp1 = 641; var NeUpWidth1 = 210;
var NeHome = 525; var NeHomeWidth = 240;

var Aelian = 650;
var FrAelian = 651;
var ItAelian = 652;
var SpAelian = 654;

var GreekRef1 = 670;
var FrGreekRef1 = 671;
var ItGreekRef1 = 672;
var SpGreekRef1 = 674;
var GreekTrans1 = 675; var GreekTransWidth1 = 240;
var FrGreekTrans1 = 676;
var ItGreekTrans1 = 677;
var SpGreekTrans1 = 679;

var GreekRef2 = 680;
var FrGreekRef2 = 681;
var ItGreekRef2 = 682;
var SpGreekRef2 = 684;
var GreekRef2PlusTranslation = 685; //KEEP. Use for texts with translations into languages other than English
var FrGreekRef2PlusTranslation = 686;
var ItGreekRef2PlusTranslation = 687;
var SpGreekRef2PlusTranslation = 689;

var EPlusG = 690; var EPlusGWidth = 240;
var FrEPlusG = 691;
var ItEPlusG = 692;
var LaEPlusG = 693;
var SpEPlusG = 694;
var EPlusG2 = 695;
var FrEPlusG2 = 696;
var ItEPlusG2 = 697;
var LaEPlusG2 = 698;
var SpEPlusG2 = 699;

var GPlusE = 700;
var FrGPlusE = 701;
var ItGPlusE = 702;
var LaGPlusE = 703;
var SpGPlusE = 704;
var GPlusE2 = 705;
var FrGPlusE2 = 706;
var ItGPlusE2 = 707;
var LaGPlusE2 = 708;
var SpGPlusE2 = 709;

var PlutarchPlusG = 710; /* var PlutarchWidth = 230; */
var FrPlutarchPlusG = 286;
var ItPlutarchPlusG = 287;
var SpPlutarchPlusG = 289;

var ResGestae = 715;

var toLivius = 720;
var LenderingNote = 721;

var EnLPlusF = 730;
var LPlusF = 731;
var ItLPlusF = 732;
var LaLPlusF = 733;
var SpLPlusF = 734;
var LPlusF2 = 735;
var FrLPlusF2 = 736;
var ItLPlusF2 = 737;
var LaLPlusF2 = 738;
var SpLPlusF2 = 739;


// Ссылка выключен сайт, страница открывается в другом окне.


// Display state variables
var o3_x = 0;
var o3_y = 0;
var o3_allow = 0;
var o3_showingsticky = 0;
var o3_removecounter = 0;

// Our layer
var over = null;


// Decide browser version
var ns4 = (document.layers)? true:false;
var ns6 = (document.getElementById)? true:false;
var ie4 = (document.all)? true:false;
var ie5 = false;

// Microsoft Stupidity Check(tm).
if (ie4) {
	if (navigator.userAgent.indexOf('MSIE 5')>0) {
		ie5 = true;
	}
	if (ns6) {
		ns6 = false;
	}
}


// Capture events, alt. diffuses the overlib function.
if ( (ns4) || (ie4) || (ns6)) {
	document.onmousemove = mouseMove
	if (ns4) document.captureEvents(Event.MOUSEMOVE)
} else {
	Ebox = no_box;
	nd = no_box;
	ver3fix = true;
}


// Fake function for 3.0 users.
function no_box() {
	return ver3fix;
}



////////////////////////////////////
// PUBLIC FUNCTIONS
////////////////////////////////////


// Ebox(arg0, ..., argN)
// Loads parameters into global runtime variables.
function Ebox() {
	
	// Load defaults to runtime.
	o3_text = ol_text;
	o3_cap = ol_cap;
	o3_sticky = ol_sticky;
	o3_background = ol_background;
	o3_close = ol_close;
	o3_hpos = ol_hpos;
	o3_offsetx = ol_offsetx;
	o3_offsety = ol_offsety;
	o3_fgcolor = ol_fgcolor;
	o3_bgcolor = ol_bgcolor;
	o3_textcolor = ol_textcolor;
	o3_capcolor = ol_capcolor;
	o3_closecolor = ol_closecolor;
	o3_width = ol_width;
	o3_border = ol_border;
	o3_status = ol_status;
	o3_autostatus = ol_autostatus;
	o3_height = ol_height;
	o3_snapx = ol_snapx;
	o3_snapy = ol_snapy;
	o3_fixx = ol_fixx;
	o3_fixy = ol_fixy;
	o3_fgbackground = ol_fgbackground;
	o3_bgbackground = ol_bgbackground;
	o3_padxl = ol_padxl;
	o3_padxr = ol_padxr;
	o3_padyt = ol_padyt;
	o3_padyb = ol_padyb;
	o3_fullhtml = ol_fullhtml;
	o3_vpos = ol_vpos;
	o3_aboveheight = ol_aboveheight;
	o3_capicon = ol_capicon;
	o3_textfont = ol_textfont;
	o3_captionfont = ol_captionfont;
	o3_closefont = ol_closefont;
	o3_textsize = ol_textsize;
	o3_captionsize = ol_captionsize;
	o3_closesize = ol_closesize;
	o3_timeout = ol_timeout;
	o3_function = ol_function;
	o3_delay = ol_delay;
	o3_hauto = ol_hauto;
	o3_vauto = ol_vauto;



	// Special for frame support, over must be reset...
	if ( (ns4) || (ie4) || (ns6) ) {
		o3_frame = ol_frame;
		if (ns4) over = o3_frame.document.overDiv
		if (ie4) over = o3_frame.overDiv.style
		if (ns6) over = o3_frame.document.getElementById("overDiv");
	}
	
	
	// What the next argument is expected to be.
	var parsemode = -1;
	
	var ar = arguments;

	for (i = 0; i < ar.length; i++) {
		
		if (parsemode == 0) {
			// Arg is command
			if (ar[i] == INARRAY) { parsemode = INARRAY; }
			if (ar[i] == CAPARRAY) { parsemode = CAPARRAY; }
			if (ar[i] == STICKY) { parsemode = opt_STICKY(ar[i]); }
			if (ar[i] == BACKGROUND) { parsemode = BACKGROUND; }
			if (ar[i] == NOCLOSE) { parsemode = opt_NOCLOSE(ar[i]); }
			if (ar[i] == CAPTION) { parsemode = CAPTION; }
			if (ar[i] == LEFT) { parsemode = opt_HPOS(ar[i]); }
			if (ar[i] == RIGHT) { parsemode = opt_HPOS(ar[i]); }
			if (ar[i] == CENTER) { parsemode = opt_HPOS(ar[i]); }
			if (ar[i] == OFFSETX) { parsemode = OFFSETX; }
			if (ar[i] == OFFSETY) { parsemode = OFFSETY; }
			if (ar[i] == FGCOLOR) { parsemode = FGCOLOR; }
			if (ar[i] == BGCOLOR) { parsemode = BGCOLOR; }
			if (ar[i] == TEXTCOLOR) { parsemode = TEXTCOLOR; }
			if (ar[i] == CAPCOLOR) { parsemode = CAPCOLOR; }
			if (ar[i] == CLOSECOLOR) { parsemode = CLOSECOLOR; }
			if (ar[i] == WIDTH) { parsemode = WIDTH; }
			if (ar[i] == BORDER) { parsemode = BORDER; }
			if (ar[i] == STATUS) { parsemode = STATUS; }
			if (ar[i] == AUTOSTATUS) { parsemode = opt_AUTOSTATUS(ar[i]); }
			if (ar[i] == AUTOSTATUSCAP) { parsemode = opt_AUTOSTATUSCAP(ar[i]); }
			if (ar[i] == HEIGHT) { parsemode = HEIGHT; }
			if (ar[i] == CLOSETEXT) { parsemode = CLOSETEXT; }
			if (ar[i] == SNAPX) { parsemode = SNAPX; }
			if (ar[i] == SNAPY) { parsemode = SNAPY; }
			if (ar[i] == FIXX) { parsemode = FIXX; }
			if (ar[i] == FIXY) { parsemode = FIXY; }
			if (ar[i] == FGBACKGROUND) { parsemode = FGBACKGROUND; }
			if (ar[i] == BGBACKGROUND) { parsemode = BGBACKGROUND; }
			if (ar[i] == PADX) { parsemode = PADX; }
			if (ar[i] == PADY) { parsemode = PADY; }
			if (ar[i] == FULLHTML) { parsemode = opt_FULLHTML(ar[i]); }
			if (ar[i] == ABOVE) { parsemode = opt_VPOS(ar[i]); }
			if (ar[i] == BELOW) { parsemode = opt_VPOS(ar[i]); }
			if (ar[i] == CAPICON) { parsemode = CAPICON; }
			if (ar[i] == TEXTFONT) { parsemode = TEXTFONT; }
			if (ar[i] == CAPTIONFONT) { parsemode = CAPTIONFONT; }
			if (ar[i] == CLOSEFONT) { parsemode = CLOSEFONT; }
			if (ar[i] == TEXTSIZE) { parsemode = TEXTSIZE; }
			if (ar[i] == CAPTIONSIZE) { parsemode = CAPTIONSIZE; }
			if (ar[i] == CLOSESIZE) { parsemode = CLOSESIZE; }
			if (ar[i] == FRAME) { parsemode = FRAME; }
			if (ar[i] == TIMEOUT) { parsemode = TIMEOUT; }
			if (ar[i] == FUNCTION) { parsemode = FUNCTION; }
			if (ar[i] == DELAY) { parsemode = DELAY; }
			if (ar[i] == HAUTO) { parsemode = opt_HAUTO(ar[i]); }
			if (ar[i] == VAUTO) { parsemode = opt_VAUTO(ar[i]); }


		} else {
			if (parsemode < 0) {
				// Arg is maintext, unless INARRAY
				if (ar[i] == INARRAY) {
					parsemode = INARRAY;
				} else {
					o3_text = ar[i];
					parsemode = 0;
				}
			} else {
				// Arg is option for command
				if (parsemode == INARRAY) { parsemode = opt_INARRAY(ar[i]); }
				if (parsemode == CAPARRAY) { parsemode = opt_CAPARRAY(ar[i]); }
				if (parsemode == BACKGROUND) { parsemode = opt_BACKGROUND(ar[i]); }
				if (parsemode == CAPTION) { parsemode = opt_CAPTION(ar[i]); }
				if (parsemode == OFFSETX) { parsemode = opt_OFFSETX(ar[i]); }
				if (parsemode == OFFSETY) { parsemode = opt_OFFSETY(ar[i]); }
				if (parsemode == FGCOLOR) { parsemode = opt_FGCOLOR(ar[i]); }
				if (parsemode == BGCOLOR) { parsemode = opt_BGCOLOR(ar[i]); }
				if (parsemode == TEXTCOLOR) { parsemode = opt_TEXTCOLOR(ar[i]); }
				if (parsemode == CAPCOLOR) { parsemode = opt_CAPCOLOR(ar[i]); }
				if (parsemode == CLOSECOLOR) { parsemode = opt_CLOSECOLOR(ar[i]); }
				if (parsemode == WIDTH) { parsemode = opt_WIDTH(ar[i]); }
				if (parsemode == BORDER) { parsemode = opt_BORDER(ar[i]); }
				if (parsemode == STATUS) { parsemode = opt_STATUS(ar[i]); }
				if (parsemode == HEIGHT) { parsemode = opt_HEIGHT(ar[i]); }
				if (parsemode == CLOSETEXT) { parsemode = opt_CLOSETEXT(ar[i]); }
				if (parsemode == SNAPX) { parsemode = opt_SNAPX(ar[i]); }
				if (parsemode == SNAPY) { parsemode = opt_SNAPY(ar[i]); }
				if (parsemode == FIXX) { parsemode = opt_FIXX(ar[i]); }
				if (parsemode == FIXY) { parsemode = opt_FIXY(ar[i]); }
				if (parsemode == FGBACKGROUND) { parsemode = opt_FGBACKGROUND(ar[i]); }
				if (parsemode == BGBACKGROUND) { parsemode = opt_BGBACKGROUND(ar[i]); }
				if (parsemode == PADX2) { parsemode = opt_PADX2(ar[i]); } // must be before PADX
				if (parsemode == PADY2) { parsemode = opt_PADY2(ar[i]); } // must be before PADY
				if (parsemode == PADX) { parsemode = opt_PADX(ar[i]); }
				if (parsemode == PADY) { parsemode = opt_PADY(ar[i]); }
				if (parsemode == CAPICON) { parsemode = opt_CAPICON(ar[i]); }
				if (parsemode == TEXTFONT) { parsemode = opt_TEXTFONT(ar[i]); }
				if (parsemode == CAPTIONFONT) { parsemode = opt_CAPTIONFONT(ar[i]); }
				if (parsemode == CLOSEFONT) { parsemode = opt_CLOSEFONT(ar[i]); }
				if (parsemode == TEXTSIZE) { parsemode = opt_TEXTSIZE(ar[i]); }
				if (parsemode == CAPTIONSIZE) { parsemode = opt_CAPTIONSIZE(ar[i]); }
				if (parsemode == CLOSESIZE) { parsemode = opt_CLOSESIZE(ar[i]); }
				if (parsemode == FRAME) { parsemode = opt_FRAME(ar[i]); }
				if (parsemode == TIMEOUT) { parsemode = opt_TIMEOUT(ar[i]); }
                                if (parsemode == FUNCTION) { parsemode = opt_FUNCTION(ar[i]); }
				if (parsemode == DELAY) { parsemode = opt_DELAY(ar[i]); }

			}
		}
	}

	if (o3_delay == 0) {
		return box333();
	} else {
		o3_delayid = setTimeout("box333()", o3_delay);

		if (o3_sticky) {
			return false;
		} else {
			return true;
		}
	}
}



// Clears popups if appropriate
function nd() {
	if ( o3_removecounter >= 1 ) { o3_showingsticky = 0 };
	if ( (ns4) || (ie4) || (ns6) ) {
		if ( o3_showingsticky == 0 ) {
			o3_allowmove = 0;
			if (over != null) hideObject(over);
		} else {
			o3_removecounter++;
		}
	}
	
	return true;
}







////////////////////////////////////
// OVERLIB 3.33 FUNCTION
////////////////////////////////////


// This function decides what it is we want to display and how we want it done.
function box333() {

	// Make layer content
	var layerhtml;

	if (o3_background != "" || o3_fullhtml) {
		// Use background instead of box.
		layerhtml = ol_content_background(o3_text, o3_background, o3_fullhtml);
	} else {
		// They want a popup box.

		// Prepare popup background
		if (o3_fgbackground != "") {
			o3_fgbackground = "BACKGROUND=\""+o3_fgbackground+"\"";
		}
		if (o3_bgbackground != "") {
			o3_bgbackground = "BACKGROUND=\""+o3_bgbackground+"\"";
		}

		// Prepare popup colors
		if (o3_fgcolor != "") {
			o3_fgcolor = "BGCOLOR=\""+o3_fgcolor+"\"";
		}
		if (o3_bgcolor != "") {
			o3_bgcolor = "BGCOLOR=\""+o3_bgcolor+"\"";
		}

		// Prepare popup height
		if (o3_height > 0) {
			o3_height = "HEIGHT=" + o3_height;
		} else {
			o3_height = "";
		}

		// Decide which kinda box.
		if (o3_cap == "") {
			// Plain
			layerhtml = ol_content_simple(o3_text);
		} else {
			// With caption
			if (o3_sticky) {
				// Show close text
				layerhtml = ol_content_caption(o3_text, o3_cap, o3_close);
			} else {
				// No close text
				layerhtml = ol_content_caption(o3_text, o3_cap, "");
			}
		}
	}
	
	// We want it to stick!
	if (o3_sticky) {
		o3_showingsticky = 1;
		o3_removecounter = 0;
	}
	
	// Write layer
	layerWrite(layerhtml);
	
	// Prepare status bar
	if (o3_autostatus > 0) {
		o3_status = o3_text;
		if (o3_autostatus > 1) {
			o3_status = o3_cap;
		}
	}

	// When placing the layer the first time, even stickies may be moved.
	o3_allowmove = 0;

	// Initiate a timer for timeout
	if (o3_timeout > 0) {          
		if (o3_timerid > 0) clearTimeout(o3_timerid);
		o3_timerid = setTimeout("cClick()", o3_timeout);
	}

	// Show layer
	disp(o3_status);

	// Stickies should stay where they are.	
	if (o3_sticky) {
		o3_allowmove = 0;
		return false;
	} else {
		return true;
	}
}



////////////////////////////////////
// LAYER GENERATION FUNCTIONS
////////////////////////////////////

// Makes simple table without caption
function ol_content_simple(text) {
	txt = "<TABLE WIDTH="+o3_width+" BORDER=0 CELLPADDING="+o3_border+" CELLSPACING=0 "+o3_bgcolor+" "+o3_height+"><TR><TD><TABLE CLASS=prompt WIDTH=100% BORDER=0 CELLPADDING=2 CELLSPACING=0 "+o3_fgcolor+" "+o3_fgbackground+" "+o3_height+"><TR><TD VALIGN=TOP><FONT FACE=\""+o3_textfont+"\" COLOR=\""+o3_textcolor+"\" SIZE=\""+o3_textsize+"\">"+text+"</SPAN></TD></TR></TABLE></TD></TR></TABLE>";
	set_background("");
	return txt;
}

// Makes table with caption and optional close link
function ol_content_caption(text, title, close) {
	closing = "";
	if (close != "") {
		closing = "<TD ALIGN=RIGHT><A HREF=\"/\" onMouseOver=\"cClick();\"><FONT COLOR=\""+o3_closecolor+"\" FACE=\""+o3_closefont+"\" SIZE=\""+o3_closesize+"\">"+close+"</SPAN></A></TD>";
	}
	if (o3_capicon != "") {
		o3_capicon = "<IMG SRC=\""+o3_capicon+"\"> ";
	}
	txt = "<TABLE WIDTH="+o3_width+" BORDER=0 CELLPADDING="+o3_border+" CELLSPACING=0 "+o3_bgcolor+" "+o3_bgbackground+" "+o3_height+"><TR><TD><TABLE WIDTH=100% BORDER=0 CELLPADDING=0 CELLSPACING=0><TR><TD><B><FONT COLOR=\""+o3_capcolor+"\" FACE=\""+o3_captionfont+"\" SIZE=\""+o3_captionsize+"\">"+o3_capicon+title+"</SPAN></B></TD>"+closing+"</TR></TABLE><TABLE WIDTH=100% BORDER=0 CELLPADDING=2 CELLSPACING=0 "+o3_fgcolor+" "+o3_fgbackground+" "+o3_height+"><TR><TD VALIGN=TOP><FONT COLOR=\""+o3_textcolor+"\" FACE=\""+o3_textfont+"\" SIZE=\""+o3_textsize+"\">"+text+"</SPAN></TD></TR></TABLE></TD></TR></TABLE>";
	set_background("");
	return txt;
}

// Sets the background picture, padding and lots more :)
function ol_content_background(text, picture, hasfullhtml) {
	if (hasfullhtml) {
		txt = text;
	} else {
		txt = "<TABLE WIDTH="+o3_width+" BORDER=0 CELLPADDING=0 CELLSPACING=0 HEIGHT="+o3_height+"><TR><TD COLSPAN=3 HEIGHT="+o3_padyt+"></TD></TR><TR><TD WIDTH="+o3_padxl+"></TD><TD VALIGN=TOP WIDTH="+(o3_width-o3_padxl-o3_padxr)+"><FONT FACE=\""+o3_textfont+"\" COLOR=\""+o3_textcolor+"\" SIZE=\""+o3_textsize+"\">"+text+"</SPAN></TD><TD WIDTH="+o3_padxr+"></TD></TR><TR><TD COLSPAN=3 HEIGHT="+o3_padyb+"></TD></TR></TABLE>";
	}
	set_background(picture);
	return txt;
}

// Loads a picture into the div.
function set_background(pic) {
	if (pic == "") {
		if (ie4) over.backgroundImage = "none";
		if (ns6) over.style.backgroundImage = "none";
	} else {
		if (ns4) {
			over.background.src = pic;
		} else if (ie4) {
			over.backgroundImage = "url("+pic+")";
		} else if (ns6) {
			over.style.backgroundImage = "url("+pic+")";
		}
	}
}



////////////////////////////////////
// HANDLING FUNCTIONS
////////////////////////////////////


// Displays the popup
function disp(statustext) {
	if ( (ns4) || (ie4) || (ns6) ) {
		if (o3_allowmove == 0) 	{
			placeLayer();
			showObject(over);
			o3_allowmove = 1;
		}
	}

	if (statustext != "") {
		self.status = statustext;
	}
}

// Decides where we want the popup.
function placeLayer() {
	var placeX, placeY;
	
	// HORIZONTAL PLACEMENT
	if (o3_fixx > -1) {
		// Fixed position
		placeX = o3_fixx;
	} else {
		winoffset = (ie4) ? o3_frame.document.body.scrollLeft : o3_frame.pageXOffset;
		if (ie4) iwidth = o3_frame.document.body.clientWidth;
		if (ns4) iwidth = o3_frame.innerWidth; // was screwed in mozilla, fixed now?
		if (ns6) iwidth = o3_frame.outerWidth;
		
		// If HAUTO, decide what to use.
		if (o3_hauto == 1) {
			if ( (o3_x - winoffset) > ((eval(iwidth)) / 2)) {
				o3_hpos = LEFT;
			} else {
				o3_hpos = RIGHT;
			}
		}
		
		// From mouse
		if (o3_hpos == CENTER) { // Center
			placeX = o3_x+o3_offsetx-(o3_width/2);
		}
		if (o3_hpos == RIGHT) { // Right
			placeX = o3_x+o3_offsetx;
			if ( (eval(placeX) + eval(o3_width)) > (winoffset + iwidth) ) {
				placeX = iwidth + winoffset - o3_width;
				if (placeX < 0) placeX = 0;
			}
		}
		if (o3_hpos == LEFT) { // Left
			placeX = o3_x-o3_offsetx-o3_width;
			if (placeX < winoffset) placeX = winoffset;
		}
	
		// Snapping!
		if (o3_snapx > 1) {
			var snapping = placeX % o3_snapx;
			if (o3_hpos == LEFT) {
				placeX = placeX - (o3_snapx + snapping);
			} else {
				// CENTER and RIGHT
				placeX = placeX + (o3_snapx - snapping);
			}
			if (placeX < 0) placeX = 0;
		}
	}

	
	
	// VERTICAL PLACEMENT
	if (o3_fixy > -1) {
		// Fixed position
		placeY = o3_fixy;
	} else {
		// If VAUTO, decide what to use.
		if (o3_vauto == 1) {
			if (ie4) iheight = o3_frame.document.body.clientHeight;
			if (ns4) iheight = o3_frame.innerHeight;
			if (ns6) iheight = o3_frame.outerHeight;

			iheight = (eval(iheight)) / 2;
			if (o3_y > iheight) {
				o3_vpos = ABOVE;
			} else {
				o3_vpos = BELOW;
			}
		}

		// From mouse
		if (o3_aboveheight > 0 && o3_vpos == ABOVE) {
			placeY = o3_y - (o3_aboveheight + o3_offsety);
		} else {
			// BELOW
			placeY = o3_y + o3_offsety;
		}

		// Snapping!
		if (o3_snapy > 1) {
			var snapping = placeY % o3_snapy;
			
			if (o3_aboveheight > 0 && o3_vpos == ABOVE) {
				placeY = placeY - (o3_snapy + snapping);
			} else {
				placeY = placeY + (o3_snapy - snapping);
			}
			
			if (placeY < 0) placeY = 0;
		}
	}


	// Actually move the object.	
	repositionTo(over, placeX, placeY);
}


// Moves the layer
function mouseMove(e) {
	if ( (ns4) || (ns6) ) {o3_x=e.pageX; o3_y=e.pageY;}
	if (ie4) {o3_x=event.x; o3_y=event.y;}
	if (ie5) {o3_x=event.x+o3_frame.document.body.scrollLeft; o3_y=event.y+o3_frame.document.body.scrollTop;}
	
	if (o3_allowmove == 1) {
		placeLayer();
	}
}

// The Close onMouseOver function for stickies
function cClick() {
	hideObject(over);
	o3_showingsticky = 0;
}


// Makes sure target frame has overLIB
function compatibleframe(frameid) {        
	if (ns4) {
		if (typeof frameid.document.overDiv =='undefined') return false;
	} else if (ie4) {
		if (typeof frameid.document.all["overDiv"] =='undefined') return false;
	} else if (ns6) {
		if (frameid.document.getElementById('overDiv') == null) return false;
	}

	return true;
}



////////////////////////////////////
// LAYER FUNCTIONS
////////////////////////////////////


// Writes to a layer
function layerWrite(txt) {
	txt += "\n";
	
        if (ns4) {
                var lyr = o3_frame.document.overDiv.document

                lyr.write(txt)
                lyr.close()
        } else if (ie4) {
		o3_frame.document.all["overDiv"].innerHTML = txt
	} else if (ns6) {
		range = o3_frame.document.createRange();
		range.setStartBefore(over);
		domfrag = range.createContextualFragment(txt);
		while (over.hasChildNodes()) {
			over.removeChild(over.lastChild);
		}
		over.appendChild(domfrag);
	}
}

// Make an object visible
function showObject(obj) {
        if (ns4) obj.visibility = "show";
        else if (ie4) obj.visibility = "visible";
	else if (ns6) obj.style.visibility = "visible";
}

// Hides an object
function hideObject(obj) {
        if (ns4) obj.visibility = "hide";
        else if (ie4) obj.visibility = "hidden";
	else if (ns6) obj.style.visibility = "hidden";
	if (o3_timerid > 0) clearTimeout(o3_timerid);
	if (o3_delayid > 0) clearTimeout(o3_delayid);
	o3_timerid = 0;
	o3_delayid = 0;
        self.status = "";
}

// Move a layer
function repositionTo(obj,xL,yL) {
	if ( (ns4) || (ie4) ) {
	        obj.left = xL;
	        obj.top = yL;
	} else if (ns6) {
		obj.style.left = xL + "px";
		obj.style.top = yL+ "px";
	}
}



////////////////////////////////////
// PARSER FUNCTIONS
////////////////////////////////////


// Sets text from array.
function opt_INARRAY(id) {
	o3_text = ol_texts[id];
	return 0;
}

// Sets caption from array.
function opt_CAPARRAY(id) {
	o3_cap = ol_caps[id];	
	return 0;
}

// Sets stickiness.
function opt_STICKY(unused) {
	o3_sticky = 1;
	return 0;
}

// Sets background picture.
function opt_BACKGROUND(file) {
	o3_background = file;
	return 0;
}

// Sets use of close text.
function opt_NOCLOSE(unused) {
	o3_close = "";
	return 0;
}

// Sets caption.
function opt_CAPTION(text) {
	o3_cap = text;
	return 0;
}

// Sets hpos, for LEFT, RIGHT and CENTER.
function opt_HPOS(pos) {
	o3_hpos = pos;
	return 0;
}

// Sets the x offset
function opt_OFFSETX(offset) {
	o3_offsetx = offset;
	return 0;
}

// Sets the y offset
function opt_OFFSETY(offset) {
	o3_offsety = offset;
	return 0;
}


// Sets the fg color
function opt_FGCOLOR(clr) {
	o3_fgcolor = clr;
	return 0;
}

// Sets the bg color
function opt_BGCOLOR(clr) {
	o3_bgcolor = clr;
	return 0;
}

// Sets the text color
function opt_TEXTCOLOR(clr) {
	o3_textcolor = clr;
	return 0;
}

// Sets the caption color
function opt_CAPCOLOR(clr) {
	o3_capcolor = clr;
	return 0;
}

// Sets the close color
function opt_CLOSECOLOR(clr) {
	o3_closecolor = clr;
	return 0;
}

// Sets the popup width
function opt_WIDTH(pixels) {
	o3_width = pixels;
	return 0;
}

// Sets the popup border width
function opt_BORDER(pixels) {
	o3_border = pixels;
	return 0;
}

// Sets the status bar text
function opt_STATUS(text) {
	o3_status = text;
	return 0;
}

// Sets that status bar text to the text
function opt_AUTOSTATUS(val) {
	o3_autostatus = 1;
	return 0;
}

// Sets that status bar text to the caption
function opt_AUTOSTATUSCAP(val) {
	o3_autostatus = 2;
	return 0;
}

// Sets the popup height
function opt_HEIGHT(pixels) {
	o3_height = pixels;
	o3_aboveheight = pixels;
	return 0;
}

// Sets the close text.
function opt_CLOSETEXT(text) {
	o3_close = text;
	return 0;
}

// Sets horizontal snapping
function opt_SNAPX(pixels) {
	o3_snapx = pixels;
	return 0;
}

// Sets vertical snapping
function opt_SNAPY(pixels) {
	o3_snapy = pixels;
	return 0;
}

// Sets horizontal position
function opt_FIXX(pos) {
	o3_fixx = pos;
	return 0;
}

// Sets vertical position
function opt_FIXY(pos) {
	o3_fixy = pos;
	return 0;
}

// Sets the fg background
function opt_FGBACKGROUND(picture) {
	o3_fgbackground = picture;
	return 0;
}

// Sets the bg background
function opt_BGBACKGROUND(picture) {
	o3_bgbackground = picture;
	return 0;
}

// Sets the left x padding for background
function opt_PADX(pixels) {
	o3_padxl = pixels;
	return PADX2;
}

// Sets the top y padding for background
function opt_PADY(pixels) {
	o3_padyt = pixels;
	return PADY2;
}

// Sets the right x padding for background
function opt_PADX2(pixels) {
	o3_padxr = pixels;
	return 0;
}

// Sets the bottom y padding for background
function opt_PADY2(pixels) {
	o3_padyb = pixels;
	return 0;
}

// Sets that user provides full html.
function opt_FULLHTML(unused) {
	o3_fullhtml = 1;
	return 0;
}

// Sets vpos, for ABOVE and BELOW
function opt_VPOS(pos) {
	o3_vpos = pos;
	return 0;
}

// Sets the caption icon.
function opt_CAPICON(icon) {
	o3_capicon = icon;
	return 0;
}

// Sets the text font
function opt_TEXTFONT(fontname) {
	o3_textfont = fontname;
	return 0;
}

// Sets the caption font
function opt_CAPTIONFONT(fontname) {
	o3_captionfont = fontname;
	return 0;
}

// Sets the close font
function opt_CLOSEFONT(fontname) {
	o3_closefont = fontname;
	return 0;
}

// Sets the text font size
function opt_TEXTSIZE(fontsize) {
	o3_textsize = fontsize;
	return 0;
}

// Sets the caption font size
function opt_CAPTIONSIZE(fontsize) {
	o3_captionsize = fontsize;
	return 0;
}

// Sets the close font size
function opt_CLOSESIZE(fontsize) {
	o3_closesize = fontsize;
	return 0;
}

// Defines which frame we should point to.
function opt_FRAME(frm) {
        o3_frame = compatibleframe(frm) ? frm : ol_frame;

	if ( (ns4) || (ie4 || (ns6)) ) {
		if (ns4) over = o3_frame.document.overDiv;
		if (ie4) over = o3_frame.overDiv.style;
		if (ns6) over = o3_frame.document.getElementById("overDiv");
	}

	return 0;
}

// Sets the popup timeout (note: 1 sec = 1000)
function opt_TIMEOUT(maxtime) {
	o3_timeout = maxtime;
	return 0;
}

// Calls an external function
function opt_FUNCTION(callme) {
	o3_text = callme()
	return 0;
}

// Sets the popup delay (note: 1 sec = 1000)
function opt_DELAY(waittime) {
	o3_delay = waittime;
	return 0;
}

// Sets the auto horizontal option
function opt_HAUTO(onoff) {
	if (o3_hauto == 0) {
		o3_hauto = 1;
	} else {
		o3_hauto = 0;
	}
	return 0;
}

// Sets the auto vertical option
function opt_VAUTO(onoff) {
	if (o3_vauto == 0) {
		o3_vauto = 1;
	} else {
		o3_vauto = 0;
	}
	return 0;
}


//end (OF OVERLIB. OTHER ITEMS MAY FOLLOW)


// Opens a single window of parametered size, called "pannellino"
function makeWindow(W,H) {
	if (W == null) { W = 567; }
	if (H == null) { H = 378; }
W = W+16;
H = H+16;
window.open("","pannellino","width="+W+",height="+H+",innerwidth="+W+",innerheight="+H+",titlebar=no,title=no,resizable=no");
}

// Opens multiple windows of parametered size, each called "pannellinoN" (N = 1, 2, etc.)
// used in SMIGRA Coma
function makeWindow1(W,H,N) {
	if (W == null) { W = 567; }
	if (H == null) { H = 378; }
N = "pannellino"+N;
W = W+16;
H = H+16;
window.open("",N,"width="+W+",height="+H+",innerwidth="+W+",innerheight="+H+",titlebar=no,title=no,resizable=no");
}

// Opens a single window of parametered size, called "pannellone"
function makeWindow2(W,H) {
	if (W == null) { W = 567; }
	if (H == null) { H = 378; }
W = W+16;
H = H+16;
window.open("","pannellone","width="+W+",height="+H+",innerwidth="+W+",innerheight="+H+",titlebar=no,title=no,resizable=no");
}

