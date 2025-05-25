package main

import (
	"bufio"
	"fmt"
	"net/http"
	"os"
	"strings"
	"sync"
)

func checkURL(url string, ident int, wg *sync.WaitGroup) {
	defer wg.Done()

	client := &http.Client{
		CheckRedirect: func(req *http.Request, via []*http.Request) error {
			return http.ErrUseLastResponse
		},
	}

	currentURL := url
	for i := range 10 {
		resp, err := client.Get(currentURL)
		if err != nil {
			// fmt.Fprintf(os.Stderr, ...
			fmt.Printf("[%4d] Error connecting to %s: %v\n", ident, currentURL, err)
			return
		}
		indent := strings.Repeat(" ", i*3)
		// Report only errors or redirects
		if resp.StatusCode != http.StatusOK || i > 0 {
			fmt.Printf("[%4d] %s%d %s\n", ident, indent, resp.StatusCode, currentURL)
		}
		// Check if this is a redirect
		if resp.StatusCode >= 300 && resp.StatusCode < 400 {
			// TODO: preserve #anchor (a.k.a. fragment identifier)
			location := resp.Header.Get("Location")
			resp.Body.Close()

			if location == "" {
				// No location header, stop following
				return
			}

			currentURL = location
		} else {
			// Not a redirect, we're done
			resp.Body.Close()
			return
		}
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

	ident := 1
	for scanner.Scan() {
		url := strings.TrimSpace(scanner.Text())
		if url == "" {
			continue
		}

		wg.Add(1)
		go checkURL(url, ident, &wg)
		ident++
	}

	wg.Wait()

	if err := scanner.Err(); err != nil {
		fmt.Fprintf(os.Stderr, "Error reading file: %v\n", err)
	}
}
