package main

import (
	"bufio"
	"fmt"
	"net/http"
	"net/url"
	"os"
	"strings"
	"sync"
)

func checkURL(rawURL string, taskId int, wg *sync.WaitGroup) {
	defer wg.Done()

	const maxRedirects = 10

	client := &http.Client{
		CheckRedirect: func(req *http.Request, via []*http.Request) error {
			return http.ErrUseLastResponse
		},
	}

	parsedURL, err := url.Parse(rawURL) // parse URL to keep #fragment-id

	if err != nil {
		fmt.Fprintf(os.Stderr, "Error parsing URL %s: %v\n", rawURL, err)
		return
	}

	currentURL := rawURL
	redirectCount := 0
	location := "" // preserve Location header to assert end of redirects
	for redirectCount = range maxRedirects {
		resp, err := client.Head(currentURL)
		if err != nil {
			fmt.Printf("[%4d] *ERROR* %v\n", taskId, err)
			break
		}
		indent := strings.Repeat(" ", redirectCount*3)
		if resp.StatusCode != http.StatusOK || redirectCount > 0 { // report only errors or redirects
			fmt.Printf("[%4d] %s%d %s\n", taskId, indent, resp.StatusCode, currentURL)
		}
		location = resp.Header.Get("Location")
		if resp.StatusCode >= 300 && resp.StatusCode < 400 { // got a redirect
			if location == "" { // no location header, stop following
				break
			}
			currentURL = location
			if parsedURL.Fragment != "" {
				currentURL += "#" + parsedURL.Fragment
			}
		} else { // not a redirect, we're done
			break
		}
	}
	if location != "" {
		panic(fmt.Sprintf("After %d redirects, Location header is still set: %s", redirectCount, location))
	}
}

func main() {
	if len(os.Args) < 2 {
		fmt.Fprintf(os.Stderr, "Usage: %s <filename>\n", os.Args[0])
		os.Exit(1)
	}

	filename := os.Args[1]
	file, err := os.Open(filename)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error opening file: %v\n", err)
		os.Exit(1)
	}
	defer file.Close()

	var wg sync.WaitGroup
	scanner := bufio.NewScanner(file)

	taskId := 1
	for scanner.Scan() {
		url := strings.TrimSpace(scanner.Text())
		if url == "" {
			continue
		}

		wg.Add(1)
		go checkURL(url, taskId, &wg)
		taskId++
	}

	wg.Wait()

	if err := scanner.Err(); err != nil {
		fmt.Fprintf(os.Stderr, "Error reading file: %v\n", err)
	}
}
