def export_to_file(self, node_name, target_dir):
   target_path = Path(target_dir)
   node = self.ct.find_node_by_name(node_name)

   if not node:
     return f'Cannot find node {node_name}'

   identifier = uuid4().hex[:8]
   outputfile = target_path.joinpath(node_name.replace(' ', '_').lower()).with_suffix('.md')
   if outputfile.exists():
     print(f'{str(outputfile)} already exists')
   outputfile=str(outputfile)
   content = "\n".join([t for t in node.texts if len(t) > 0])
   try:
     pypandoc.convert_text(content,
             'markdown',
             format='markdown',
             outputfile=outputfile,
             extra_args=[
               f'metadata=identifier:{identifier}',
               f'metadata=title:{node.name}',
               'defaults=create_document'
             ])
   except Exception as e:
     return e
   [e.getparent().remove(e) for e in node.element.iterchildren('rich_text')]
   anchor = node.insert_anchor(identifier)
   node.insert_link(href=outputfile, text="Content")
   self.ct.save()
   return f'Notes from {node.name} written to {outputfile}'
