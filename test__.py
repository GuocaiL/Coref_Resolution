import re
text = u"<DOC DOCNO=\"nw/xinhua/00/chtb_0036@0036@xinhua@nw@ch@on\"><TEXT PARTNO=\"000\"><COREF ID=\"8\" TYPE=\"IDENT\"><COREF ID=\"1\" TYPE=\"" \
       u"IDENT\">澳</COREF> 外长</COREF> 说 <COREF ID=\"1\" TYPE=\"IDENT\">澳</COREF> 坚持 <COREF ID=\"4\" TYPE=\"IDENT\"><COREF ID=\"5\" TYPE=\"IDENT\"" \
       u">一 个 <COREF ID=\"5\" TYPE=\"IDENT\">中国</COREF></COREF> <COREF ID=\"4\" TYPE=\"IDENT\">政策</COREF></COREF>新华社 堪培拉 ４月 １２日 电<COREF " \
       u"ID=\"8\" TYPE=\"IDENT\"><COREF ID=\"chtb_036.fid.utf8.source-E1\" TYPE=\"APPOS\" SUBTYPE=\"ATTRIB\"><COREF ID=\"1\" TYPE=\"IDENT\">澳大利亚" \
       u"</COREF> <COREF ID=\"8\" TYPE=\"IDENT\">外长</COREF></COREF> <COREF ID=\"chtb_036.fid.utf8.source-E1\" TYPE=\"APPOS\" SUBTYPE=\"HEAD\">唐纳" \
       u"</COREF></COREF> 日前 在 悉尼 说 ， <COREF ID=\"15\" TYPE=\"IDENT\"><COREF ID=\"1\" TYPE=\"IDENT\">澳</COREF> <COREF ID=\"15\" TYPE=\"IDENT\">" \
       u"政府</COREF></COREF> 将 坚持 <COREF ID=\"4\" TYPE=\"IDENT\"><COREF ID=\"5\" TYPE=\"IDENT\">一 个 <COREF ID=\"5\" TYPE=\"IDENT\">中国</COREF>" \
       u"</COREF> 的 <COREF ID=\"4\" TYPE=\"IDENT\">政策</COREF></COREF> ， <COREF ID=\"22\" TYPE=\"IDENT\"><COREF ID=\"23\" TYPE=\"IDENT\">澳 中</COREF>" \
       u" <COREF ID=\"22\" TYPE=\"IDENT\">关系</COREF></COREF> 是 <COREF ID=\"25\" TYPE=\"IDENT\"><COREF ID=\"26\" TYPE=\"IDENT\"><COREF ID=\"1\" " \
       u"TYPE=\"IDENT\">澳</COREF> <COREF ID=\"26\" TYPE=\"IDENT\">外交 政策</COREF></COREF> 的 一 个 <COREF ID=\"25\" TYPE=\"IDENT\">中心点</COREF>" \
       u"</COREF> 。<COREF ID=\"8\" TYPE=\"IDENT\">唐纳</COREF> 是 <COREF ID=\"31\" TYPE=\"IDENT\">*OP* *T*-2 在 *pro* 对 外国 记者 阐述 <COREF ID=\"35\" " \
       u"TYPE=\"IDENT\"><COREF ID=\"36\" TYPE=\"IDENT\"><COREF ID=\"1\" TYPE=\"IDENT\">澳</COREF> 对 <COREF ID=\"38\" TYPE=\"IDENT\">亚洲</COREF> " \
       u"<COREF ID=\"36\" TYPE=\"IDENT\">政策</COREF></COREF> 的 <COREF ID=\"35\" TYPE=\"IDENT\">框架</COREF></COREF> 时 说 <COREF ID=\"31\" TYPE=\"IDENT\"" \
       u">这 番 <COREF ID=\"31\" TYPE=\"IDENT\">话</COREF></COREF> 的</COREF> 。<COREF ID=\"8\" TYPE=\"IDENT\">他</COREF> 说 ， *PRO* 加强 <COREF ID=\"45\"" \
       u" TYPE=\"IDENT\">双边 <COREF ID=\"45\" TYPE=\"IDENT\">关系</COREF></COREF> 是 <COREF ID=\"47\" TYPE=\"IDENT\"><COREF ID=\"48\" TYPE=\"IDENT\">" \
       u"<COREF ID=\"15\" TYPE=\"IDENT\"><COREF ID=\"1\" TYPE=\"IDENT\">澳大利亚</COREF> 新 <COREF ID=\"15\" TYPE=\"IDENT\">政府</COREF></COREF> 对 " \
       u"<COREF ID=\"38\" TYPE=\"IDENT\">亚洲</COREF> 和 <COREF ID=\"54\" TYPE=\"IDENT\">世界 其它 <COREF ID=\"54\" TYPE=\"IDENT\">地区</COREF></COREF>" \
       u" <COREF ID=\"48\" TYPE=\"IDENT\">政策</COREF></COREF> 的 主要 <COREF ID=\"47\" TYPE=\"IDENT\">特点 之一</COREF></COREF> 。<COREF ID=\"8\" " \
       u"TYPE=\"IDENT\">他</COREF> 特别 提到 了 <COREF ID=\"1\" TYPE=\"IDENT\">澳大利亚</COREF> 拟 *PRO* 加强 <COREF ID=\"62\" TYPE=\"IDENT\">与 <COREF " \
       u"ID=\"63\" TYPE=\"IDENT\">中国 、 印尼 、 日本 、 韩国 和 印度 等 <COREF ID=\"38\" TYPE=\"IDENT\">亚洲</COREF> <COREF ID=\"63\" TYPE=\"IDENT\">国家" \
       u"</COREF></COREF> 的 双边 <COREF ID=\"62\" TYPE=\"IDENT\">关系</COREF></COREF> 。<COREF ID=\"8\" TYPE=\"IDENT\">他</COREF> 说 ， *OP* *T*-1 新 " \
       u"当选 的 自由党 和 国家党 联盟 政府 将 鼓励 *PRO* 与 <COREF ID=\"5\" TYPE=\"IDENT\">中国</COREF> 全面 发展 <COREF ID=\"75\" TYPE=\"IDENT\">贸易 和 " \
       u"投资 <COREF ID=\"75\" TYPE=\"IDENT\">联系</COREF></COREF> ， 合作 领域 包括 基础 行业 、 加工业 和 服务业 等 。<COREF ID=\"15\" TYPE=\"IDENT\">" \
       u"<COREF ID=\"1\" TYPE=\"IDENT\">澳</COREF> <COREF ID=\"15\" TYPE=\"IDENT\">政府</COREF></COREF> 将 继续 促进 <COREF ID=\"83\" TYPE=\"IDENT\">" \
       u"<COREF ID=\"84\" TYPE=\"IDENT\"><COREF ID=\"23\" TYPE=\"IDENT\">澳 中</COREF> <COREF ID=\"84\" TYPE=\"IDENT\">经济</COREF></COREF> 的 " \
       u"<COREF ID=\"83\" TYPE=\"IDENT\">互补性 合作</COREF></COREF> ， 并 开辟 <COREF ID=\"88\" TYPE=\"IDENT\"><COREF ID=\"89\" TYPE=\"IDENT\">澳 华 " \
       u"<COREF ID=\"89\" TYPE=\"IDENT\">商界</COREF></COREF> 与 <COREF ID=\"5\" TYPE=\"IDENT\">中国</COREF> 的 <COREF ID=\"88\" TYPE=\"IDENT\">联系" \
       u"</COREF></COREF> 。（ 完 ）</TEXT></DOC>"

cop2 = re.compile('<[^/][\s\w\."=-]*">')
s = cop2.sub('', text)
print(s)