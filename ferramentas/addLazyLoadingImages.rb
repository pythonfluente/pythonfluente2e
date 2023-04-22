class AddLazyLoadingImages < (Asciidoctor::Converter.for 'html5')
  register_for 'html5'

  def convert_image node
    target = node.attr 'target'
    width_attr = (node.attr? 'width') ? %( width="#{node.attr 'width'}") : ''
    height_attr = (node.attr? 'height') ? %( height="#{node.attr 'height'}") : ''

    # https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/loading
    loading_attr_value = (node.attr 'loading') || (node.document.attr 'image-loading')
    if loading_attr_value && loading_attr_value != 'eager' && loading_attr_value != 'lazy'
      logger.warn 'valid values for attribute "loading" are "eager" and "lazy". found: ' + loading_attr_value
    end
    loading_attr = loading_attr_value ? %( loading="#{loading_attr_value}") : ''

    if ((node.attr? 'format', 'svg') || (target.include? '.svg')) && node.document.safe < SafeMode::SECURE
      if node.option? 'inline'
        img = (read_svg_contents node, target) || %(<span class="alt">#{node.alt}</span>)
      elsif node.option? 'interactive'
        fallback = (node.attr? 'fallback') ? %(<img src="#{node.image_uri node.attr 'fallback'}" alt="#{encode_attribute_value node.alt}"#{width_attr}#{height_attr}#{loading_attr}#{@void_element_slash}>) : %(<span class="alt">#{node.alt}</span>)
        img = %(<object type="image/svg+xml" data="#{src = node.image_uri target}"#{width_attr}#{height_attr}>#{fallback}</object>)
      else
        img = %(<img src="#{src = node.image_uri target}" alt="#{encode_attribute_value node.alt}"#{width_attr}#{height_attr}#{loading_attr}#{@void_element_slash}>)
      end
    else
      img = %(<img src="#{src = node.image_uri target}" alt="#{encode_attribute_value node.alt}"#{width_attr}#{height_attr}#{loading_attr}#{@void_element_slash}>)
    end
    if (node.attr? 'link') && ((href_attr_val = node.attr 'link') != 'self' || (href_attr_val = src))
      img = %(<a class="image" href="#{href_attr_val}"#{(append_link_constraint_attrs node).join}>#{img}</a>)
    end
    id_attr = node.id ? %( id="#{node.id}") : ''
    classes = ['imageblock']
    classes << (node.attr 'float') if node.attr? 'float'
    classes << %(text-#{node.attr 'align'}) if node.attr? 'align'
    classes << node.role if node.role
    class_attr = %( class="#{classes.join ' '}")
    title_el = node.title? ? %(\n<div class="title">#{node.captioned_title}</div>) : ''
    %(<div#{id_attr}#{class_attr}>
<div class="content">
#{img}
</div>#{title_el}
</div>)
  end

  def convert_inline_image node
    target = node.target
    if (type = node.type || 'image') == 'icon'
      if (icons = node.document.attr 'icons') == 'font'
        i_class_attr_val = %(fa fa-#{target})
        i_class_attr_val = %(#{i_class_attr_val} fa-#{node.attr 'size'}) if node.attr? 'size'
        if node.attr? 'flip'
          i_class_attr_val = %(#{i_class_attr_val} fa-flip-#{node.attr 'flip'})
        elsif node.attr? 'rotate'
          i_class_attr_val = %(#{i_class_attr_val} fa-rotate-#{node.attr 'rotate'})
        end
        attrs = (node.attr? 'title') ? %( title="#{node.attr 'title'}") : ''
        img = %(<i class="#{i_class_attr_val}"#{attrs}></i>)
      elsif icons
        attrs = (node.attr? 'width') ? %( width="#{node.attr 'width'}") : ''
        attrs = %(#{attrs} height="#{node.attr 'height'}") if node.attr? 'height'
        attrs = %(#{attrs} title="#{node.attr 'title'}") if node.attr? 'title'
        img = %(<img src="#{src = node.icon_uri target}" alt="#{encode_attribute_value node.alt}"#{attrs}#{@void_element_slash}>)
      else
        img = %([#{node.alt}&#93;)
      end
    else
      attrs = (node.attr? 'width') ? %( width="#{node.attr 'width'}") : ''
      attrs = %(#{attrs} height="#{node.attr 'height'}") if node.attr? 'height'
      attrs = %(#{attrs} title="#{node.attr 'title'}") if node.attr? 'title'

      # https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/loading
      loading_attr_value = (node.attr 'loading') || (node.document.attr 'image-loading')
      if loading_attr_value && loading_attr_value != 'eager' && loading_attr_value != 'lazy'
        logger.warn 'valid values for attribute "loading" are "eager" and "lazy". found: ' + loading_attr_value
      end
      attrs = %(#{attrs} loading="#{loading_attr_value}") if loading_attr_value

      if ((node.attr? 'format', 'svg') || (target.include? '.svg')) && node.document.safe < SafeMode::SECURE
        if node.option? 'inline'
          img = (read_svg_contents node, target) || %(<span class="alt">#{node.alt}</span>)
        elsif node.option? 'interactive'
          fallback = (node.attr? 'fallback') ? %(<img src="#{node.image_uri node.attr 'fallback'}" alt="#{encode_attribute_value node.alt}"#{attrs}#{@void_element_slash}>) : %(<span class="alt">#{node.alt}</span>)
          img = %(<object type="image/svg+xml" data="#{src = node.image_uri target}"#{attrs}>#{fallback}</object>)
        else
          img = %(<img src="#{src = node.image_uri target}" alt="#{encode_attribute_value node.alt}"#{attrs}#{@void_element_slash}>)
        end
      else
        img = %(<img src="#{src = node.image_uri target}" alt="#{encode_attribute_value node.alt}"#{attrs}#{@void_element_slash}>)
      end
    end
    if (node.attr? 'link') && ((href_attr_val = node.attr 'link') != 'self' || (href_attr_val = src))
      img = %(<a class="image" href="#{href_attr_val}"#{(append_link_constraint_attrs node).join}>#{img}</a>)
    end
    class_attr_val = type
    if (role = node.role)
      class_attr_val = (node.attr? 'float') ? %(#{class_attr_val} #{node.attr 'float'} #{role}) : %(#{class_attr_val} #{role})
    elsif node.attr? 'float'
      class_attr_val = %(#{class_attr_val} #{node.attr 'float'})
    end
    %(<span class="#{class_attr_val}">#{img}</span>)
  end
end
