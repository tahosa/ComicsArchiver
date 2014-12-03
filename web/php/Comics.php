<?php

namespace Comics

/**
 * Main entry point for the webcomics archive dynamic site
 */
class Comics
{
  private config;

  /**
   * Create a new instance to process request
   *
   * @param Config $config Configuration data
   */
  public function __construct(Config $config)
  {
    $this->config = $config;
  }
}
