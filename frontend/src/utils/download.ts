export const downloadFileFromHref = (href: string, fileName: string) => {
  const x = new XMLHttpRequest()
  x.open('GET', href, true)
  x.responseType = 'blob'
  x.withCredentials = true
  x.onload = () => {
    downloadFileFromBlob(x.response, fileName)
  }
  x.send()
}

export const downloadFileFromBlob = (response: Blob, filename: string) => {
  const url = window.URL.createObjectURL(response)
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', filename)
  document.body.appendChild(link)
  link.click()

  // clean up "a" element & remove ObjectURL
  document.body.removeChild(link)
  URL.revokeObjectURL(url)
}
