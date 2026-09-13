"""Reusable restrained Chinese Word styling; requires python-docx.
Apply to a new Document, then author content and independently render/inspect.
"""
from docx.shared import Cm,Pt,RGBColor
from docx.oxml.ns import qn
def apply_reading_styles(document,source_version):
 if not source_version.strip():raise ValueError('Explicit paper version required')
 document.core_properties.subject=source_version
 for section in document.sections:
  section.page_width=Cm(21);section.page_height=Cm(29.7)
  section.top_margin=section.bottom_margin=Cm(2.1)
  section.left_margin=section.right_margin=Cm(2.4)
 for name,size in [('Normal',11.5),('Title',22),('Heading 1',16),('Heading 2',13),('Heading 3',12),('Caption',10)]:
  s=document.styles[name];s.font.name='Times New Roman';s.font.size=Pt(size);s.font.color.rgb=RGBColor(0,0,0)
  s._element.get_or_add_rPr().rFonts.set(qn('w:eastAsia'),'黑体' if name.startswith('Heading') else '宋体')
  s.font.bold=name.startswith('Heading');s.paragraph_format.widow_control=True;s.paragraph_format.space_after=Pt(7)
  s.paragraph_format.line_spacing=1.2 if name=='Caption' else 1.5
  if name.startswith('Heading'):s.paragraph_format.keep_with_next=True;s.font.bold=True
 for s in document.styles:
  for border in list(s._element.iter(qn('w:pBdr'))):border.getparent().remove(border)
 return document
