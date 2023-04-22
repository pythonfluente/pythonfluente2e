include Asciidoctor

class AddLazyLoadingImages < Asciidoctor::Extensions::Postprocessor
  def process document, output
    if document.basebackend? 'html'
      replacement = %(<img loading="lazy" \\1>)
      output = output.gsub(/<img(.*?)>/m, replacement)
    end
    output
  end
end

Asciidoctor::Extensions.register do
  postprocessor AddLazyLoadingImages
end

Asciidoctor.convert_file 'livro.adoc', safe: :safe


