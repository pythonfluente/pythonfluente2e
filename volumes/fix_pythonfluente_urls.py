"""
In the volume 1 *.adoc files, find links in this form:

```
fpy.li/2p?{ref}[{text}] (vol. {vol}, cap. {ch_num})
```

Replace them with:

```
_{text} (vol.{vol}, cap.{ch_num}, fpy.li/{su})_
```

(vol.2, cap.13, fpy.li/q7)

Where {su} is the short URL for a URL to `pythonfluente.com`, such as:

```
https://pythonfluente.com/2/#{ref}
```

"""